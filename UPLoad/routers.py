from rest_framework import routers

from user.viewsets import AuthViewSet, GoogleAuthViewSet, ProfileViewSet
from reports.viewsets import ReportViewSet
from reports_v2.views import FormViewSet,FieldsViewSet, ResponseViewSet, ResponseDocumentViewSet

router = routers.SimpleRouter()

router.register(r'user', AuthViewSet, basename="user")
router.register(r'user/google', GoogleAuthViewSet, basename="google")
router.register(r'profile', ProfileViewSet, basename="profile")
router.register(r'report', ReportViewSet, basename="report")
router.register(r'forms',FormViewSet, basename='forms')
router.register(r'fields',FieldsViewSet, basename='fields')
router.register(r'responses',ResponseViewSet, basename='responses')
router.register(r'documents',ResponseDocumentViewSet, basename='documents')

urlpatterns = router.urls