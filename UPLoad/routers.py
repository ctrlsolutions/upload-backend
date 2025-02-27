from rest_framework import routers

from user.viewsets import CustomUserViewSet

router = routers.SimpleRouter()

router.register(r'user', CustomUserViewSet, basename="user")

urlpatterns = router.urls