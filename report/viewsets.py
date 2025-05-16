# views.py
import json
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Form, Field, Response as ResponseModel, ResponseDocument, Report
from .serializers import FormSerializer, FieldSerializer, ResponseSerializer, ResponseDocumentSerializer
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from .utils.generate_pdf import generate_merged_pdf
from django.http import FileResponse
import os
    
class ResponseViewSet(viewsets.ModelViewSet):
    serializer_class = ResponseSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # You can filter based on query params, like form_id or user_id, if needed
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
    
    @action(detail=False, methods=['post'], url_path='generate-pdf')
    def generate_pdf(self, request):
        data = request.data
        scope = data.get('scope')
        timeframe = data.get('timeframe')
        items = []

        ## BASIC SECTION
        if scope == "self":
            items = Report.objects.get(user=request.user)
        elif scope == "department":
            items = Report.objects.get(department=request.user.department)

        sections = [
            ("report/basic.html", {"scope": scope, "timeframe": timeframe}),
        ]

        ## REPORT LIST SECTION
        if scope == "self":
            items = Report.objects.get(user=request.user)
        elif scope == "department":
            items = Report.objects.get(department=request.user.department)

        sections.append(("report/reportlist.html", {"items": items}))

        merged_pdf = generate_merged_pdf(sections)

        response = FileResponse(merged_pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="full_report.pdf"'

        # Clean up after sending
        def cleanup(f):
            f.close()
            os.unlink(f.name)
        response.close = lambda *args, **kwargs: cleanup(merged_pdf)

        return response
    
    ## TODO: frontend and backend

class FormViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    def list(self, request):
        forms = Form.objects.prefetch_related('fields').all()
        serializer = FormSerializer(forms, many=True)
        return Response(serializer.data)