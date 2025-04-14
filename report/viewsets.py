from django.db import models
from .models import Report
from .serializers import ReportHistorySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets

class ReportViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'], url_path='history', permission_classes=[IsAuthenticated])
    def report_history(self, request):
        user = request.user
        user_role = user.role.code if user.role else None

        
        if user_role == 'F': # Faculty
            reports = Report.objects.filter(user_id=user)
        
        elif user_role == 'DP': # Department Chair
            reports = Report.objects.filter(
                models.Q(user_id=user) | models.Q(department_id=user.department_id)
            )

        elif user_role == 'CD': # College Dean
            reports = Report.objects.filter(
                models.Q(user_id=user) | models.Q(college_id=user.college_id)
            )

        elif user_role == 'C': # Chancellor
            reports = Report.objects.all()


        else:
            # default to own reports only if role is missing or unrecognized
            reports = Report.objects.filter(user_id=user)

        reports = reports.select_related('user_id__college', 'user_id__department')
        serializer = ReportHistorySerializer(reports, many=True)
        return Response(serializer.data)
