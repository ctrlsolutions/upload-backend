from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return Response({
            "error": response.data.get("detail", "An unexpected error occurred"),
        }, status=response.status_code)

    return Response({
        "error": "An unhandled exception occurred"
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
