from rest_framework import viewsets, status, serializers, permissions

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils.decorators import method_decorator

from .models import Report
from .serializers import ReportHistorySerializer
from rest_framework.viewsets import ViewSet

class ReportViewSet(viewsets.ViewSet):
    
    @action(detail=False, methods=['get'], url_path='history', permission_classes=[IsAuthenticated])
    def report_history(self, request):
        """
        Endpoint to retrieve the history of all reports.
        URL: GET /api/reports/history/
        """
        reports = Report.objects.all()
        serializer = ReportHistorySerializer(reports, many=True)
        return Response(serializer.data)

