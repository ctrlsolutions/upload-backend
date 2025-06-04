# views.py
import json
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Form, Field, Response as ResponseModel, ResponseDocument, Report
from .serializers import FormSerializer, ResponseSerializer, ResponseDocumentSerializer
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from .utils.basic_new import generate_report
from .utils.reportlist import generate_report as generate_reportlist
from django.http import FileResponse
from django.db.models import Count
from django.utils import timezone
import tempfile, os
from PyPDF2 import PdfMerger

import os
from django.conf import settings
from datetime import datetime

def generate_pdf_path(user, part):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{user.username}-{timestamp}-part{part}.pdf"
    return os.path.join(settings.MEDIA_ROOT, filename)


def stream_and_cleanup(file_path, download_name):
    def file_iterator():
        with open(file_path, 'rb') as f:
            yield from f
        os.remove(file_path)

    return FileResponse(file_iterator(), as_attachment=True, filename=download_name)

    
class ResponseViewSet(viewsets.ModelViewSet):
    serializer_class = ResponseSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        form_id = self.request.query_params.get('form_id', None)
        if form_id:
            return ResponseModel.objects.filter(form_id=form_id)
        return ResponseModel.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user if request.user.is_authenticated else None
        response_data = data.get('response')
        form_id = data.get('form')

        if not form_id:
            return Response({"detail": "form_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            form = Form.objects.get(id=form_id)
        except Form.DoesNotExist:
            return Response({"detail": "Form not found."}, status=status.HTTP_404_NOT_FOUND)

        # Create the response entry
        response_instance = ResponseModel.objects.create(
            user=user,
            form=form,
            response=response_data
        )

        # Handle file uploads
        for key in request.FILES:
            uploaded_file = request.FILES[key]
            ResponseDocument.objects.create(
                response=response_instance,
                file=uploaded_file
            )

        serializer = self.get_serializer(response_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ResponseDocumentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset that provides `list` and `retrieve` actions for response documents.
    """
    queryset = ResponseDocument.objects.all()
    serializer_class = ResponseDocumentSerializer
    permission_classes = [permissions.AllowAny]  # Change this if you want to restrict access

    def get_queryset(self):
        # Optional filtering by response_id via query parameter
        response_id = self.request.query_params.get('response_id')
        if response_id:
            return self.queryset.filter(response_id=response_id)
        return self.queryset
    
class ReportViewSet(viewsets.ViewSet):
    def create(self, request):
        user = request.user

        form_id = request.data.get('form')
        department = request.user.department
        college = request.user.college
        response_raw = request.data.get('response')
        
        if not all([form_id, response_raw]):
            return Response({'error': 'Missing required fields.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response_data = json.loads(response_raw)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid response format.'}, status=status.HTTP_400_BAD_REQUEST)

        form = get_object_or_404(Form, id=form_id)

        form_response = ResponseModel.objects.create(
            form=form,
            user=user,
            response=response_data
        )

        title_field = Field.objects.filter(form=form, code='report_title').first()
        title_value = response_data.get(str(title_field.id)) if title_field else form.name

        report = Report.objects.create(
            title=title_value,
            user=user,
            department=department,
            college=college,
            form=form,
            response=form_response
        )

        supporting_documents = [file for key, file in request.FILES.items() if key.startswith('document_')]
        for file in supporting_documents:
            ResponseDocument.objects.create(
                response=form_response,
                file=file
            )

        return Response({
            'message': 'Report submitted successfully.',
            'report_id': report.id
        }, status=status.HTTP_201_CREATED)

    def list(self, request):
        # GET ALL REPORTS OF USER 
        # CHECK USER ROLE
        # IF DEP HEAD, GET ALL REPORTS OF DEPARTMENT
        # IF COLLEGE DEAN, GET ALL REPORTS OF COLLEGE
        # ...
        pass
        
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        user = request.user
        data = request.data
        scope = data.get("scope")
        timeframe = data.get("timeframe")  # handle this as needed
        reports = Report.objects.none()

        ## BASIC SECTION
        if scope == "FA":
            reports = Report.objects.filter(user=user)
        elif scope == "DH":
            reports = Report.objects.filter(department=user.department)
        elif scope == "CD":
            reports = Report.objects.filter(college=user.college)
        elif scope == "CH":
            reports = Report.objects.all()

        items_qs = (
            reports.values("form__name")
            .annotate(number_of_submissions=Count("id"))
            .order_by("form__name")
        )

        SCOPE_LABELS = {
            "FA": "Self",
            "DH": "Department",
            "CD": "College",
            "CH": "University",
        }

        TIMEFRAME_LABELS = {
            "SM": "6 months",
            "YR": "1 year",
        }


        items = [
            {"type": entry["form__name"], "number_of_submissions": entry["number_of_submissions"]}
            for entry in items_qs if entry["form__name"]  # filter out possible nulls
        ]
        submissions = reports.order_by("created_on").values_list("created_on", flat=True)
        from collections import Counter
        date_counts = Counter([dt.date().isoformat() for dt in submissions])

        submissions_data = sorted(date_counts.items())

        context = {
            "scope": SCOPE_LABELS.get(scope, scope),
            "department": user.department.name if user.department else "",
            "college": user.college.name if user.college else "",
            "university": "UP Cebu",  # or fetch dynamically
            "timeframe": TIMEFRAME_LABELS.get(timeframe, timeframe),
            "generated_by": f"{user.first_name} {user.middle_name[0] + '.' if user.middle_name else ''} {user.last_name}",
            "generated_on": timezone.now().strftime('%m-%d-%Y'),
            "items": items,
            "submissions": submissions_data,
        }

        detailed_submissions = [
            {
                "type": report.form.name if report.form else "Unknown",
                "title": report.title,
                "submitted_by": f"{report.user.first_name} {report.user.last_name}",
                "date_submitted": report.created_on.strftime('%Y-%m-%d')
            }
            for report in reports.select_related("user", "form")
        ]

        con = {
            "scope": SCOPE_LABELS.get(scope, scope),
            "department": user.department.name if user.department else "",
            "college": user.college.name if user.college else "",
            "university": "UP Cebu",  # or fetch dynamically
            "timeframe": TIMEFRAME_LABELS.get(timeframe, timeframe),
            "generated_by": f"{user.first_name} {user.middle_name[0] + '.' if user.middle_name else ''} {user.last_name}",
            "generated_on": timezone.now().strftime('%m-%d-%Y'),
            "detailed_submissions": detailed_submissions
        }


        print(context)

        timestamp = timezone.now().strftime("%Y%m%d-%H%M%S")
        base_name = f"{user.username}-{timestamp}"
        
        pdf1_path = generate_pdf_path(user, 1)
        # generate_report(context, pdf1_path)

        pdf2_path = generate_pdf_path(user, 2)
        # generate_reportlist(con, pdf2_path)
        
        final_pdf_path = generate_pdf_path(user, 3)

        try:
        # generate PDFs (make sure these functions close the file internally)
            generate_report(context, pdf1_path)
            generate_reportlist(con, pdf2_path)

            # combine them
            merger = PdfMerger()
            with open(pdf1_path, 'rb') as f1, open(pdf2_path, 'rb') as f2:
                merger.append(f1)
                merger.append(f2)
                with open(final_pdf_path, 'wb') as fout:
                    merger.write(fout)
            merger.close()

            # Clean up part1 and part2 safely
            os.remove(pdf1_path)
            os.remove(pdf2_path)

            return stream_and_cleanup(final_pdf_path, f"{base_name}.pdf")

        except Exception as e:
            # Optional: clean up if something goes wrong
            for path in [pdf1_path, pdf2_path, final_pdf_path]:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except Exception:
                        pass
            raise e
        # ## REPORT LIST SECTION
        # if scope == "self":
        #     items = Report.objects.filter(user=request.user)
        #     print(items)
        # elif scope == "department":
        #     items = Report.objects.get(department=request.user.department)

        # sections.append(("report/reportlist.html", {"items": items}))

        # merged_pdf = generate_merged_pdf(sections)

        # response = FileResponse(merged_pdf, content_type='application/pdf')
        # response['Content-Disposition'] = 'attachment; filename="full_report.pdf"'

        # Clean up after sending
        # def cleanup(f):
        #     f.close()
        #     os.unlink(f.name)
        # response.close = lambda *args, **kwargs: cleanup(merged_pdf)

        return response
    
    ## TODO: frontend and backend

class FormViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    def list(self, request):
        forms = Form.objects.prefetch_related('fields').all()
        serializer = FormSerializer(forms, many=True)
        return Response(serializer.data)