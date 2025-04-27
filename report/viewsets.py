# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Form, Field, Response as ResponseModel, ResponseDocument, ReportFormTemplate, Report
from .serializers import FormSerializer, FieldSerializer, ResponseSerializer, ResponseDocumentSerializer, ReportFormTemplateSerializer, ReportSerializer
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
    
# class ResponseViewSet(viewsets.ModelViewSet):
#     serializer_class = ResponseSerializer
#     permission_classes = [permissions.AllowAny]

#     def get_queryset(self):
#         # You can filter based on query params, like form_id or user_id, if needed
#         form_id = self.request.query_params.get('form_id', None)
#         if form_id:
#             return ResponseModel.objects.filter(form_id=form_id)
#         return ResponseModel.objects.all()

#     def create(self, request, *args, **kwargs):
#         data = request.data
#         user = request.user if request.user.is_authenticated else None
#         response_data = data.get('response')
#         form_id = data.get('form')

#         if not form_id:
#             return Response({"detail": "form_id is required."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             form = Form.objects.get(id=form_id)
#         except Form.DoesNotExist:
#             return Response({"detail": "Form not found."}, status=status.HTTP_404_NOT_FOUND)

#         # Create the response entry
#         response_instance = ResponseModel.objects.create(
#             user=user,
#             form=form,
#             response=response_data
#         )

#         # Handle file uploads
#         for key in request.FILES:
#             uploaded_file = request.FILES[key]
#             ResponseDocument.objects.create(
#                 response=response_instance,
#                 file=uploaded_file
#             )

#         serializer = self.get_serializer(response_instance)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = ResponseModel.objects.all()
    serializer_class = ResponseSerializer


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
    def list(self, request):
        reports = Report.objects.all().order_by('created_on')  # Replace 'date' with the actual field name if needed
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)


class FormTemplateViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    def list(self, request):
        templates = ReportFormTemplate.objects.select_related('form').prefetch_related('form__fields').all()
        serializer = ReportFormTemplateSerializer(templates, many=True)
        return Response(serializer.data)