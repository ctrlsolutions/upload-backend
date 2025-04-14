from rest_framework import routers

from user.viewsets import AuthViewSet, GoogleAuthViewSet, ProfileViewSet
from reports.viewsets import ReportViewSet, ReportHistoryViewSet 

router = routers.SimpleRouter()

router.register(r'user', AuthViewSet, basename="user")
router.register(r'user/google', GoogleAuthViewSet, basename="google")
router.register(r'profile', ProfileViewSet, basename="profile")
router.register(r'report-history', ReportViewSet, basename='report') 
router.register(r'report-history', ReportHistoryViewSet, basename='report-history') 

urlpatterns = router.urls