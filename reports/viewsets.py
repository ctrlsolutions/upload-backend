from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

from .models import Report, ResearchReport, PublicationReport, OthersReport
from .serializers import (
    ResearchSerializer,
    PublicationSerializer,
    OthersSerializer
)
class ResearchReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Research Reports.
    Handles CRUD operations for ResearchReport, including the nested Report creation/update.
    """
    queryset = ResearchReport.objects.select_related('report_id').all() # Use the correct related name from model
    serializer_class = ResearchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Optionally filter reports to only show those belonging to the current user.
        """
        user = self.request.user
        if user.is_authenticated:
            # Filter based on the user associated with the base Report
            return ResearchReport.objects.select_related('report_id').filter(report_id__user_id=user)
            # If using the related_name 'report' in the serializer field, but 'report_id' in model:
            # return ResearchReport.objects.select_related('report_id').filter(report_id__user_id=user)
        return ResearchReport.objects.none() # Or handle anonymous users differently

    # The .create(), .update(), .partial_update(), .destroy(), .list(), .retrieve()
    # methods are provided by ModelViewSet. They will automatically use:
    # 1. serializer_class (ResearchSerializer)
    # 2. The serializer's .create() / .update() methods (which handle nesting)
    # 3. The request context (which provides request.user to the serializer)

class PublicationReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Publication Reports.
    """
    queryset = PublicationReport.objects.select_related('report_id').all()
    serializer_class = PublicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Optionally filter reports to only show those belonging to the current user.
        """
        user = self.request.user
        if user.is_authenticated:
            return PublicationReport.objects.select_related('report_id').filter(report_id__user_id=user)
        return PublicationReport.objects.none()

class OthersReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Other Reports.
    """
    queryset = OthersReport.objects.select_related('report_id').all()
    serializer_class = OthersSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Optionally filter reports to only show those belonging to the current user.
        """
        user = self.request.user
        if user.is_authenticated:
            return OthersReport.objects.select_related('report_id').filter(report_id__user_id=user)
        return OthersReport.objects.none()