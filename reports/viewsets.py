from rest_framework import viewsets, status, serializers, permissions

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Report, ResearchReport, PublicationReport, OthersReport
from .serializers import ReportSerializer, ResearchSerializer, PublicationSerializer, PaperSerializer, PatentSerializer, OtherResearchSerializer, TrainingSerializer, ExtensionSerializer, PartnershipSerializer, OthersSerializer


class ReportViewSet(viewsets.ViewSet):
    """
    A ViewSet for handling different types of Reports via custom actions.
    Provides separate endpoints for creating Research, Publication, and Other reports.
    """
    permission_classes = [AllowAny] #For testing purposes, change to IsAuthenticated in production
    parser_classes = [MultiPartParser, FormParser]

    def _create_specific_report(self, request, serializer_class):
        """
        Handles the common logic for creating a report using a specific serializer.
        """
        serializer = serializer_class(data=request.data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='research')
    def create_research_report(self, request):
        """
        Endpoint to create a new Research Report.
        Expects nested payload: {"report": {"title": "..."}, "timeframe": ..., ...}
        URL: POST /api/reports/research/
        """
        return self._create_specific_report(request, ResearchSerializer)

    @action(detail=False, methods=['post'], url_path='publication')
    def create_publication_report(self, request):
        """
        Endpoint to create a new Publication Report.
        Expects nested payload: {"report": {"title": "..."}, "publication_title": ..., ...}
        URL: POST /api/reports/publication/
        """
        return self._create_specific_report(request, PublicationSerializer)
    
    @action(detail=False, methods=['post'], url_path='paper_presentation')
    def create_paper_presentation_report(self, request):
        """
        Endpoint to create a new Paper Presentation Report.
        Expects nested payload: {"report": {"title": "..."}, "presentation_title": ..., ...}
        URL: POST /api/reports/paper_presentation/
        """
        return self._create_specific_report(request, PaperSerializer)
    
    @action(detail=False, methods=['post'], url_path='patent')
    def create_patent_report(self, request):
        """
        Endpoint to create a new Patent Report.
        Expects nested payload: {"report": {"title": "..."}, "patent_title": ..., ...}
        URL: POST /api/reports/patent/
        """
        return self._create_specific_report(request, PatentSerializer)
    
    @action(detail=False, methods=['post'], url_path='other_research')
    def create_other_research_report(self, request):
        """
        Endpoint to create a new Other Research Report.
        Expects nested payload: {"report": {"title": "..."}, "research_title": ..., ...}
        URL: POST /api/reports/otherresearch/
        """
        return self._create_specific_report(request, OtherResearchSerializer)
    
    @action(detail=False, methods=['post'], url_path='training')
    def create_training_report(self, request):
        """
        Endpoint to create a new Training Report.
        Expects nested payload: {"report": {"title": "..."}, "training_title": ..., ...}
        URL: POST /api/reports/training/
        """
        return self._create_specific_report(request, TrainingSerializer)
    
    @action(detail=False, methods=['post'], url_path='extension')
    def create_extension_report(self, request):
        """
        Endpoint to create a new Extension Report.
        Expects nested payload: {"report": {"title": "..."}, "extension_title": ..., ...}
        URL: POST /api/reports/extension/
        """
        return self._create_specific_report(request, ExtensionSerializer)
    
    @action(detail=False, methods=['post'], url_path='partnership')
    def create_partnership_report(self, request):
        """
        Endpoint to create a new Partnership Report.
        Expects nested payload: {"report": {"title": "..."}, "partnership_title": ..., ...}
        URL: POST /api/reports/partnership/
        """
        return self._create_specific_report(request, PartnershipSerializer)

    @action(detail=False, methods=['post'], url_path='others')
    def create_others_report(self, request):
        """
        Endpoint to create a new Others Report.
        Expects nested payload: {"report": {"title": "..."}, "description": ...}
        URL: POST /api/reports/others/
        """
        return self._create_specific_report(request, OthersSerializer)
    
