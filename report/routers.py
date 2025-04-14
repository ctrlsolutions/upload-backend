from rest_framework.routers import DefaultRouter
from .viewsets import ReportViewSet

router = DefaultRouter()
router.register(r'', ReportViewSet, basename='report')

report_router = router
