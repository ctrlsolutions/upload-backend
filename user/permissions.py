from rest_framework.permissions import BasePermission

class IsAccountOwner(BasePermission):
    """
    Custom permission to allow access only if the authenticated user matches the username in the request.
    """
    def has_permission(self, request, view):
        username_from_query = request.GET.get("username")  # ✅ Extract from query params
        print("I AM IN HAS_PERMISSION:", 
              request.user.is_authenticated, 
              request.user.username == username_from_query, 
              request.user.username, 
              username_from_query)

        return request.user.is_authenticated and request.user.username == username_from_query
