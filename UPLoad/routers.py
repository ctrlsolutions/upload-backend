from rest_framework import routers

from user.viewsets import AuthViewSet, GoogleAuthViewSet, ProfileViewSet
from report.viewsets import ResponseViewSet, ResponseDocumentViewSet, ReportViewSet, FormViewSet
from university.viewsets import CollegeDepartmentViewSet, CollegeViewSet

router = routers.SimpleRouter()

router.register(r'user', AuthViewSet, basename="user")
router.register(r'user/google', GoogleAuthViewSet, basename="google")
router.register(r'profile', ProfileViewSet, basename="profile")
router.register(r'college', CollegeViewSet, basename='college')
router.register(r'cd', CollegeDepartmentViewSet, basename='cd')
router.register(r'form', FormViewSet, basename='form')
router.register(r'report', ReportViewSet, basename='report')
router.register(r'responses',ResponseViewSet, basename='responses')
router.register(r'documents',ResponseDocumentViewSet, basename='documents')

urlpatterns = router.urls