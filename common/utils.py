import logging

from typing import Optional

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)

def api_response(data: Optional[dict] = None, message: Optional[str] = None, error: Optional[str] = None, status=status.HTTP_200_OK):
    response_data = {}
    
    if message:
        response_data["message"] = message
    if data is not None:
        response_data["data"] = data
    if error:
        response_data["success"] = False
        response_data["error"] = error
    else:
        response_data["success"] = True

    return Response(response_data, status=status)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        data = response.data

        if isinstance(data, dict):
            if "detail" in data:
                return Response({
                    "success": False,
                    "error": {
                        "non_field_error": [data["detail"]]
                    }
                }, status=response.status_code)
            else:
                return Response({
                    "success": False,
                    "error": data
                }, status=response.status_code)

    logger.error("Unhandled exception", exc_info=exc)
    return Response({
        "success": False,
        "error": {
            "non_field_error": ["An unhandled exception occurred."]
        }
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
