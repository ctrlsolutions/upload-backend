from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication

from .models import CustomUser

from .serializers import CustomUserSerializer, LoginSerializer

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse



class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authenticationClasses = [SessionAuthentication]
    permission_classes = [AllowAny]

    @method_decorator(ensure_csrf_cookie)
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def csrf(self, request):
        return JsonResponse({"message": "CSRF cookie set"})
    
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        print(email)
        print(password)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            user = None
        print(user)
        if user and user.check_password(password):
            login(request, user)
            return Response({"message": "Login successful", "user_id": user.user_id})
        else:
            return Response({"error": "Invalid credentials"})
        
    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """Logs out a user and destroys the session."""
        logout(request)
        return Response({"message": "Logged out successfully!"})
    
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def user(self, request):
        """Gets the authenticated user."""
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)