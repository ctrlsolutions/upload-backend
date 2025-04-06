from django.http import HttpResponseForbidden

class RoleHierarchyPermissionRequiredMixin:
    required_permission = None

    def dispatch(self, request, *args, **kwargs):
        if not self.check_user_permission(request.user, self.required_permission):
            return HttpResponseForbidden("You don't have permission to view this page.")
        return super().dispatch(request, *args, **kwargs)

    def check_user_permission(self, user, permission_code):
        if not user.is_authenticated:
            return False
        for role in user.roles.all():
            permissions = role.get_permissions()
            if permission_code in [perm.code_name for perm in permissions]:
                return True
        return False
