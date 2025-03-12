from rest_framework import routers

from user.viewsets import AuthViewSet, GoogleAuthViewSet, DashboardViewSet

router = routers.SimpleRouter()

router.register(r'user', AuthViewSet, basename="user")
router.register(r'user/google', GoogleAuthViewSet, basename="google")
router.register(r'dashboard', DashboardViewSet, basename="dashboard")

urlpatterns = router.urls