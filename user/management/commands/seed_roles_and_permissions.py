# yourapp/management/commands/seed_roles_and_permissions.py
from django.core.management.base import BaseCommand
from user.models import Role, Permission, RolePermission  # Adjust imports based on your model locations

class Command(BaseCommand):
    help = 'Seeds the database with initial roles and permissions'

    def handle(self, *args, **kwargs):
        # Create permissions
        # BASE PERMISSIONS
        can_view_own_reports = Permission.objects.create(name="Can view own reports", code_name="view_own_reports")
        can_edit_own_reports = Permission.objects.create(name="Can edit own reports", code_name="edit_own_reports")
        can_delete_own_reports = Permission.objects.create(name="Can delete own reports", code_name="delete_own_reports")
        can_generate_own_reports = Permission.objects.create(name="Can generate own reports", code_name="generate_own_reports")

        # DEPARTMENT HEAD LEVEL
        can_view_dep_reports = Permission.objects.create(name="Can view department reports", code_name="view_department_reports")
        can_generate_dep_reports = Permission.objects.create(name="Can generate department reports", code_name="generate_department_reports")

        # COLLEGE DEAN LEVEL
        can_view_col_reports = Permission.objects.create(name="Can view college reports", code_name="view_college_reports")
        can_generate_col_reports = Permission.objects.create(name="Can generate department_reports", code_name="generate_college_reports")

        # CHANCELLOR LEVEL
        can_view_uni_reports = Permission.objects.create(name="Can view university reports", code_name="can_view_university_reports")
        can_generate_uni_reports = Permission.objects.create(name="Can generate university reports", code_name="can_generate_university_reports")

        # ADMIN LEVEL
        can_add_departments = Permission.objects.create(name="Can add departments", code_name="add_departments")
        can_add_colleges = Permission.objects.create(name="Can add colleges", code_name="add_colleges")
        can_assign_roles = Permission.objects.create(name="Can assign user roles", code_name="assign_roles")
        can_remove_roles = Permission.objects.create(name="Can remove roles", code_name="remove_roles")
        can_add_admins = Permission.objects.create(name="Can add admins", code_name="add_admins")

        # Create roles
        admin = Role.objects.create(name="Admin", code="AD")
        chancellor = Role.objects.create(name="Chancellor", code="CH")
        college_dean = Role.objects.create(name="College Dean", code="CD", parent=chancellor)
        department_head = Role.objects.create(name="Department Head", code="DH", parent=college_dean)
        faculty = Role.objects.create(name="Faculty", code="FA", parent=department_head)
        staff = Role.objects.create(name="Staff", code="ST")
        researcher = Role.objects.create(name="Researcher", code="RE")

        # Assign permissions to roles

        ## BASE PERMS
        RolePermission.objects.create(role=faculty, permission=can_view_own_reports)
        RolePermission.objects.create(role=faculty, permission=can_edit_own_reports)
        RolePermission.objects.create(role=faculty, permission=can_delete_own_reports)
        RolePermission.objects.create(role=faculty, permission=can_generate_own_reports)
        RolePermission.objects.create(role=staff, permission=can_view_own_reports)
        RolePermission.objects.create(role=staff, permission=can_edit_own_reports)
        RolePermission.objects.create(role=staff, permission=can_delete_own_reports)
        RolePermission.objects.create(role=staff, permission=can_generate_own_reports)
        RolePermission.objects.create(role=researcher, permission=can_view_own_reports)
        RolePermission.objects.create(role=researcher, permission=can_edit_own_reports)
        RolePermission.objects.create(role=researcher, permission=can_delete_own_reports)
        RolePermission.objects.create(role=researcher, permission=can_generate_own_reports)

        ## DEPARTMENT HEAD PERMS
        RolePermission.objects.create(role=department_head, permission=can_view_dep_reports)
        RolePermission.objects.create(role=department_head, permission=can_generate_dep_reports)

        ## COLLEGE DEAN PERMS
        RolePermission.objects.create(role=college_dean, permission=can_view_col_reports)
        RolePermission.objects.create(role=college_dean, permission=can_generate_col_reports)

        ## CHANCELLOR PERMS
        RolePermission.objects.create(role=chancellor, permission=can_view_uni_reports)
        RolePermission.objects.create(role=chancellor, permission=can_generate_uni_reports)

        ## ADMIN PERMS
        RolePermission.objects.create(role=admin, permission=can_add_departments)
        RolePermission.objects.create(role=admin, permission=can_add_colleges)
        RolePermission.objects.create(role=admin, permission=can_add_admins)
        RolePermission.objects.create(role=admin, permission=can_assign_roles)
        RolePermission.objects.create(role=admin, permission=can_remove_roles)

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with roles and permissions!'))
