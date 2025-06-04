import requests

from django.contrib.auth import login, logout
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action    

from common.utils import api_response

from .serializers import (
    SignUpSerializer,
    LogInSerializer,
    UserProfileSerializer,
)
from .permissions import IsAccountOwner
from .utils import assign_predefined_role
from .models import CustomUser

GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
class AuthViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]

    @method_decorator(ensure_csrf_cookie)
    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def csrf(self, request):
        """DONE"""
        return api_response(message="CSRF cookie set")
    
    
    def create(self, request):
        """Handles both Google and regular sign-up"""
        data = request.data.copy()
        if data.get("access_token"):
            access_token = data.get("access_token")
            google_response = requests.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"}
            )

            if google_response.status_code != 200:
                return Response(
                    {"error": "Invalid access token"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            google_data = google_response.json()

            data["email"] = data.get("email") or google_data.get("email")
            data["first_name"] = data.get("first_name") or google_data.get("given_name")
            data["last_name"] = data.get("last_name") or google_data.get("family_name")
            data["google_id"] = google_data.get("sub")

        serializer = SignUpSerializer(data=data)

        if serializer.is_valid():
            user = serializer.save()
            assign_predefined_role(user)
            return api_response(
                message="Signed up successfully!",
                status=status.HTTP_201_CREATED
            )

        return api_response(
            message="There was an error signing up. Please try again.",
            error=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request):
        serializer = LogInSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)
            return api_response(message="Login successful")

        return Response(serializer.errors, status=400)

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """Logs out a user and destroys the session."""
        logout(request)
        return api_response(success=True, message="CSRF cookie set")

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated, IsAccountOwner],
    )
    def status(self, request):
        """Gets the authenticated user."""

        return Response({"message": f"Welcome {request.user.username}!"})



class GoogleAuthViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    def create(self, request):
        access_token = request.data.get("access_token")
        extra_info = request.data.get("extra_info")

        if not access_token:
            return Response(
                {"error": "Missing access token"}, status=status.HTTP_400_BAD_REQUEST
            )

        google_response = requests.get(
            GOOGLE_USERINFO_URL, headers={"Authorization": f"Bearer {access_token}"}
        )

        if google_response.status_code != 200:
            return Response(
                {"error": "Invalid access token"}, status=status.HTTP_400_BAD_REQUEST
            )

        google_data = google_response.json()

        if "email" not in google_data:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )

        email = google_data["email"]
        first_name = google_data.get("given_name", "")
        last_name = google_data.get("family_name", "")
        google_id = google_data.get("sub")

        birthdate = extra_info.get("dob")
        sex = extra_info.get("gender")
        password = extra_info.get("password")

        print("BACKEND ", extra_info, email, first_name)

        if CustomUser.objects.filter(email=email).exists():
            return Response(
                {"error": "Email is already registered"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "birthdate": birthdate,
                "sex": sex,
                "google_id": google_id,
            },
        )

        # IF DOMAIN != UP MAIL, RETURN BAD REQUEST
        if created and password:
            user.set_password(password)
            user.save()

        return Response(
            {
                "message": "Signup successful",
                # "token": access_token.token,
                "user": {
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                },
            },
            status=status.HTTP_200_OK,
        )


class ProfileViewSet(viewsets.ViewSet):
    """Handles retrieving all necessary profile data."""

    permission_classes = [IsAuthenticated]
    lookup_field = "username"

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Returns the user profile [DONE]"""
        user_data = UserProfileSerializer(request.user).data
        api_response(
            success=True,
            message="User profile fetched successfully!",
            data={"user": user_data},
        )

    @action(detail=False, methods=["patch"], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """Updates the user profile"""
        serializer = UserProfileSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return api_response(
                success=True,
                message="User profile fetched successfully!",
                data={"user": serializer.data},
            )

        return api_response(
            success=False,
            message="Profile update failed.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    def retrieve(self, request, username=None):
        user = request.user

        try:
            target_user = self.get_queryset().get(username=username)
        except CustomUser.DoesNotExist:
            return api_response(
                success=False,
                message="User not found.",
                error="User with that username does not exist.",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        # Restrict access for Department Heads
        if user.role.name.lower() == "department head":
            if not user.department or target_user.department != user.department:
                return api_response(
                    success=False,
                    message="Access denied.",
                    error="You can only view users in your department.",
                    status_code=status.HTTP_403_FORBIDDEN,
                )

        # If all checks pass, return user info
        serializer = self.get_serializer(target_user)
        return api_response(
            success=True,
            message="User retrieved successfully.",
            data={"user": serializer.data},
            status_code=status.HTTP_200_OK,
        )
