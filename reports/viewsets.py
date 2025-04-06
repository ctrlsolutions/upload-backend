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
    queryset = ResearchReport.objects.select_related('report_id').all() 
    serializer_class = ResearchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Optionally filter reports to only show those belonging to the current user.
        """
        user = self.request.user
        if user.is_authenticated:
            return ResearchReport.objects.select_related('report_id').filter(report_id__user_id=user)

        return ResearchReport.objects.none()

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