from rest_framework import routers

from user.viewsets import AuthViewSet, GoogleAuthViewSet, ProfileViewSet, CollegeDepartmentViewSet
from report.viewsets import ResponseViewSet, ResponseDocumentViewSet, ReportViewSet, FormTemplateViewSet

router = routers.SimpleRouter()

router.register(r'user', AuthViewSet, basename="user")
router.register(r'user/google', GoogleAuthViewSet, basename="google")
router.register(r'profile', ProfileViewSet, basename="profile")
router.register(r'cd', CollegeDepartmentViewSet, basename='cd')
router.register(r'report', ReportViewSet, basename='report')
router.register(r'ft', FormTemplateViewSet, basename='form-template')
router.register(r'responses',ResponseViewSet, basename='responses')
router.register(r'documents',ResponseDocumentViewSet, basename='documents')

urlpatterns = router.urls