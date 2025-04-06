from rest_framework import viewsets, status

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils.decorators import method_decorator

from .models import Report, ResearchReport, PublicationReport, OthersReport
from .serializers import SubmitReportSerializer, ResearchSerializer, PublicationSerializer, OthersSerializer

class ReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=["post"])
    def post_data(self, request):
        user = request.user 
        serializer = SubmitReportSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({
                "message": "Report submitted successfully.",
                "report": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
