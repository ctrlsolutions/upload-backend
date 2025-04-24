from .models import PredefinedRole, Role

def assign_predefined_role(user):
    try:
        mapping = PredefinedRole.objects.get(email=user.email)
        user.role = mapping.role
    except PredefinedRole.DoesNotExist:
        try:
            faculty_role = Role.objects.get(code='FA')
            user.role = faculty_role
        except Role.DoesNotExist:
            pass  # TODO: log warning or raise exception
    user.save()
