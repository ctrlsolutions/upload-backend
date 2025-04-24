from rest_framework import routers

<<<<<<< HEAD
from user.viewsets import AuthViewSet, GoogleAuthViewSet, ProfileViewSet, CollegeDepartmentViewset
from report.viewsets import ReportViewSet
=======
from user.viewsets import AuthViewSet, GoogleAuthViewSet, ProfileViewSet
from reports.viewsets import ReportViewSet
from reports_v2.views import FormViewSet,FieldsViewSet, ResponseViewSet, ResponseDocumentViewSet
>>>>>>> 1e12470 (savepoint for dynamic forms feature)

router = routers.SimpleRouter()

router.register(r'user', AuthViewSet, basename="user")
router.register(r'user/google', GoogleAuthViewSet, basename="google")
router.register(r'profile', ProfileViewSet, basename="profile")
<<<<<<< HEAD
router.register(r'reports', ReportViewSet, basename="report")
router.register(r'cd', CollegeDepartmentViewset, basename="cd")
=======
router.register(r'report', ReportViewSet, basename="report")
router.register(r'forms',FormViewSet, basename='forms')
router.register(r'fields',FieldsViewSet, basename='fields')
router.register(r'responses',ResponseViewSet, basename='responses')
router.register(r'documents',ResponseDocumentViewSet, basename='documents')
>>>>>>> 1e12470 (savepoint for dynamic forms feature)

urlpatterns = router.urls