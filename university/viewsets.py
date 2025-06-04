import requests

from django.utils.decorators import method_decorator

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from common.utils import api_response

from .serializers import CollegeDepartmentsSerializer, CollegeSerializer
from .models import College



class CollegeViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    def create(self, request):
        try:
            serializer = CollegeSerializer(data=request.data)
            if serializer.is_valid():
                college = serializer.save()

                # Notify via WebSocket
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    "college_updates",
                    {
                        "type": "college_added",
                        "data": CollegeSerializer(college).data
                    }
                )

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("🚨 Error in create():", e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CollegeDepartmentViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=["get"])
    def get_college_departments(self, request):
        """Get college/department pairs"""
        colleges = College.objects.prefetch_related("departments").all()
        serializer = CollegeDepartmentsSerializer(colleges, many=True)
        return Response(serializer.data)

def notify_college_added(college_instance):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "college_updates",
        {
            "type": "college_added",
            "data": {
                "id": college_instance.college_id,
                "code": college_instance.code,
                "name": college_instance.name,
            },
        },
    )
