# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Form, Field, Response as ResponseModel, ResponseDocument
from .serializers import FormSerializer, FieldSerializer, ResponseSerializer, ResponseDocumentSerializer
from rest_framework import permissions
from rest_framework.decorators import action

class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    permission_classes = [permissions.AllowAny] 

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class FieldsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FieldSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        form_id = self.request.query_params.get('form_id')
        if form_id:
            return Field.objects.filter(form_id=form_id)
        return Field.objects.none()
    
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