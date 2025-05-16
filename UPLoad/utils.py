from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return Response({
            "success": False,
            "error": response.data.get("detail", "An error occurred"),
            "message": None
        }, status=response.status_code)

    return response