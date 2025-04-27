from rest_framework import viewsets
from .models import CustomUser, College, Department, Role, RolePermission, Permission

from .serializers import SignUpSerializer, LogInSerializer, UserProfileSerializer, CollegeDepartmentsSerializer, DepartmentSerializer

import requests

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils.decorators import method_decorator

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .permissions import IsAccountOwner
from .utils import assign_predefined_role

class AuthViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()

    @method_decorator(ensure_csrf_cookie)
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def csrf(self, request):
        return JsonResponse({"message": "CSRF cookie set"})
    
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request):
        serializer = LogInSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)
            print(f"User authenticated: {request.user.is_authenticated}, User: {user}")
            response = JsonResponse({"message": "Login successful!", "username": user.username  })
            print(response)
            return response
        
        return Response(serializer.errors, status=400)
    
    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """Logs out a user and destroys the session."""
        logout(request)
        return Response({"message": "Logged out successfully!"})
    
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated, IsAccountOwner])
    def status(self, request):
        """Gets the authenticated user."""

        return Response({"message": f"Welcome {request.user.username}!"})
    
    # Signup action
    @method_decorator(csrf_exempt)
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def signup(self, request):
        """Creates a new user."""
        print("Request data:", request.data)  # Debugging
        serializer = SignUpSerializer(data=request.data)
                
        if serializer.is_valid():
            print("Validated data:", serializer.validated_data)
            user = serializer.save()  # Save the new user
            assign_predefined_role(user)
            return Response({"message": "User created successfully!"}, status=201)
        print("Errors:", serializer.errors)  # Debugging
        return Response(serializer.errors, status=400)
    
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

class GoogleAuthViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def signup(self, request):
        access_token = request.data.get("access_token")
        extra_info = request.data.get("extra_info")

        if not access_token:
            return Response({"error": "Missing access token"}, status=status.HTTP_400_BAD_REQUEST)

        google_response = requests.get(
        GOOGLE_USERINFO_URL,
        headers={"Authorization": f"Bearer {access_token}"}
        )

        if google_response.status_code != 200:
            return Response({"error": "Invalid access token"}, status=status.HTTP_400_BAD_REQUEST)

        google_data = google_response.json()

        if "email" not in google_data:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        email = google_data["email"]
        first_name = google_data.get("given_name", "")
        last_name = google_data.get("family_name", "")
        google_id = google_data.get("sub")

        birthdate = extra_info.get("dob")
        sex = extra_info.get("gender")
        password = extra_info.get("password")

        print("BACKEND ", extra_info, email, first_name)

        if CustomUser.objects.filter(email=email).exists():
            return Response({"error": "Email is already registered"}, status=status.HTTP_400_BAD_REQUEST)

        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "birthdate": birthdate,
                "sex": sex,
                "google_id": google_id,
            }
        )

        # IF DOMAIN != UP MAIL, RETURN BAD REQUEST
        if created and password:
            user.set_password(password)
            user.save()

        return Response(
            {
                "message": "Signup successful",
                # "token": access_token.token,
                "user": {"email": email, "first_name": first_name, "last_name": last_name},
            },
            status=status.HTTP_200_OK,
        )

class ProfileViewSet(viewsets.ViewSet):
    """Handles retrieving all necessary dashboard data in one API call."""
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def get_data(self, request):
        """Fetch all required dashboard data in one request."""
        user = request.user
        
        user_data = UserProfileSerializer(user).data
        
        return Response({
            "user": user_data,  
        })
    
    @action(detail=False, methods=["patch"], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """Update user profile"""
        user = request.user
        print(user)
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated", "user": serializer.data})
        return Response(serializer.errors, status=400)
    
class CollegeDepartmentViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=["get"])
    def get_college_departments(self, request):
        """Get college/department pairs"""
        colleges = College.objects.prefetch_related('departments').all()
        serializer = CollegeDepartmentsSerializer(colleges, many=True)
        return Response(serializer.data)
