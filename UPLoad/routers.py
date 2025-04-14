from rest_framework import routers

from user.viewsets import AuthViewSet, GoogleAuthViewSet, ProfileViewSet
from report.viewsets import ReportViewSet

router = routers.SimpleRouter()

router.register(r'user', AuthViewSet, basename="user")
router.register(r'user/google', GoogleAuthViewSet, basename="google")
router.register(r'profile', ProfileViewSet, basename="profile")
router.register(r'reports', ReportViewSet, basename='report')

urlpatterns = router.urls