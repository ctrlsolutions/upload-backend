from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import Report
from .serializers import ReportHistorySerializer

class ReportViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['get'], url_path='history', permission_classes=[IsAuthenticated])
    def report_history(self, request):
        user = request.user
        user_role = user.role.code if user.role else None

        user_reports = Report.objects.filter(user_id=user)
        user_department_ids = user_reports.values_list('department_id', flat=True).distinct()
        user_college_ids = user_reports.values_list('college_id', flat=True).distinct()

        if user_role == 'F':  # Faculty
            reports = user_reports

        elif user_role == 'DC':  # Department Chair
            reports = Report.objects.filter(
                Q(user_id=user) | Q(department_id__in=user_department_ids)
            )

        elif user_role == 'CD':  # College Dean
            reports = Report.objects.filter(
                Q(user_id=user) | Q(college_id__in=user_college_ids)
            )

        elif user_role == 'C':  # Chancellor
            reports = Report.objects.all()

        else:
            reports = user_reports

        reports = reports.select_related('user_id', 'department_id', 'college_id')
        serializer = ReportHistorySerializer(reports, many=True, context={'request': request})
        return Response(serializer.data)
