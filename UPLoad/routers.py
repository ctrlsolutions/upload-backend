from rest_framework import routers

from user.viewsets import AuthViewSet, GoogleAuthViewSet

router = routers.SimpleRouter()

router.register(r'user', AuthViewSet, basename="user")
router.register(r'user/google', GoogleAuthViewSet, basename="google")

urlpatterns = router.urls