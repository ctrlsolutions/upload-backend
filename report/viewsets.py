from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import Report
from .serializers import ReportHistorySerializer
from rest_framework import status
from rest_framework.exceptions import PermissionDenied

class ReportViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['get'], url_path='history', permission_classes=[IsAuthenticated])
    def report_history(self, request):
        user = request.user
        user_role = user.role.code if user.role else None

        if user_role == 'F':  # Faculty
            reports = Report.objects.filter(user_id=user)

        elif user_role == 'DC':  # Department Chair
            reports = Report.objects.filter(
                Q(user_id=user) | Q(department_id=user.department)
            )

        elif user_role == 'CD':  # College Dean
            reports = Report.objects.filter(
                Q(user_id=user) | Q(college_id=user.college)
            )

        elif user_role == 'C':  # Chancellor
            reports = Report.objects.all()

        else:
            reports = Report.objects.filter(user_id=user)

        reports = reports.select_related('user_id', 'department_id', 'college_id')
        serializer = ReportHistorySerializer(reports, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='delete-multiple', permission_classes=[IsAuthenticated])
    def delete_multiple(self, request):
        ids = request.data.get('ids', [])
        if not ids:
            return Response({"detail": "No report IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Only allow deleting reports owned by user
        reports = Report.objects.filter(id__in=ids, user_id=request.user)
        deleted_count = reports.count()
        reports.delete()

        return Response({"success": True, "deleted": deleted_count}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], url_path='delete-all', permission_classes=[IsAuthenticated])
    def delete_all(self, request):
        reports = Report.objects.filter(user_id=request.user)
        deleted_count = reports.count()
        reports.delete()

        return Response({"success": True, "deleted": deleted_count}, status=status.HTTP_200_OK)
