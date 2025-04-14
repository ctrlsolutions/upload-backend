from rest_framework.routers import DefaultRouter
from .viewsets import ReportHistoryViewSet

router = DefaultRouter()
router.register(r'report-history', ReportHistoryViewSet, basename='report-history')

urlpatterns = router.urls
