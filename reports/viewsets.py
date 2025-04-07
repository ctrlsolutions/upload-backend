from rest_framework import viewsets, status, serializers, permissions

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils.decorators import method_decorator

from .models import Report, ResearchReport, PublicationReport, OthersReport
from .serializers import SubmitReportSerializer, ResearchSerializer, PublicationSerializer, OthersSerializer

# class ReportViewSet(viewsets.ViewSet):
#     permission_classes = [AllowAny]
    
#     @action(detail=False, methods=["post"])
#     def post_data(self, request):
#         user = request.user 
#         serializer = SubmitReportSerializer(data=request.data)
        
#         if serializer.is_valid():
#             serializer.save(user=user)
#             return Response({
#                 "message": "Report submitted successfully.",
#                 "report": serializer.data
#             }, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReportViewSet(viewsets.ViewSet):
    """
    A ViewSet for handling different types of Reports via custom actions.
    Provides separate endpoints for creating Research, Publication, and Other reports.
    """
    permission_classes = [AllowAny]

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

    @action(detail=False, methods=['post'], url_path='others')
    def create_others_report(self, request):
        """
        Endpoint to create a new Others Report.
        Expects nested payload: {"report": {"title": "..."}, "description": ...}
        URL: POST /api/reports/others/
        """
        return self._create_specific_report(request, OthersSerializer)
