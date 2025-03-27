from rest_framework import routers

from user.viewsets import AuthViewSet, GoogleAuthViewSet, ProfileViewSet

router = routers.SimpleRouter()

router.register(r'user', AuthViewSet, basename="user")
router.register(r'user/google', GoogleAuthViewSet, basename="google")
router.register(r'profile', ProfileViewSet, basename="profile")

urlpatterns = router.urls