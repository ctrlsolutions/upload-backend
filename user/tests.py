from django.test import TestCase
from user.models import Role, Permission, RolePermission

class RoleHierarchyTest(TestCase):
    def test_admin_inherits_manager_permissions(self):
        # Create roles
        admin_role = Role.objects.create(name="Admin", code="AM")
        manager_role = Role.objects.create(name="Manager", code="MG", parent=admin_role)

        # Create a permission
        view_permission = Permission.objects.create(name="Can", code_name="can")

        # Assign permission to the Admin role
        RolePermission.objects.create(role=manager_role, permission=view_permission)

        # Assert Manager inherits Admin's permission
        self.assertTrue(view_permission in admin_role.get_permissions())

    def test_parent_inherits_child_permissions(self):
        # Create roles
        admin_role = Role.objects.create(name="Admin", code="AM")
        manager_role = Role.objects.create(name="Manager", code="MG", parent=admin_role)

        # Create permissions
        parent_perm = Permission.objects.create(name="Can refactor", code_name="can_refactor")
        child_perm = Permission.objects.create(name="Can do", code_name="can_do")
        # Assign permissions
        RolePermission.objects.create(role=admin_role, permission=parent_perm)
        RolePermission.objects.create(role=manager_role, permission=child_perm)

        # Get admin permissions (should include its own + manager's)
        permissions = admin_role.get_permissions()

        print("Admin permissions (top-down):")
        for p in permissions:
            print("-", p.name, "(", p.code_name, ")")

        assert parent_perm in permissions
        assert child_perm in permissions

class HierarchicalRolePermissionTest(TestCase):

    def setUp(self):
        self.roles = {
            role.code: role for role in Role.objects.all()
        }

    def assertHasPermissions(self, role_code, expected_codes):
        role = Role.objects.get(code=role_code)
        print(role)
        perms = role.get_permissions()
        code_names = [p.code_name for p in perms]
        self.assertTrue(set(expected_codes).issubset(code_names), f"{role_code} missing: {set(expected_codes) - perms}")

    def test_faculty_permissions(self):
        self.assertHasPermissions("FA", [
            "view_own_reports", "edit_own_reports", "delete_own_reports", "generate_own_reports"
        ])

    def test_department_head_inherits_faculty(self):
        self.assertHasPermissions("DH", [
            "view_own_reports", "edit_own_reports", "delete_own_reports", "generate_own_reports",
            "view_department_reports", "generate_department_reports"
        ])

    def test_college_dean_inherits_dh_and_fa(self):
        self.assertHasPermissions("CD", [
            "view_own_reports", "edit_own_reports", "delete_own_reports", "generate_own_reports",
            "view_department_reports", "generate_department_reports",
            "view_college_reports", "generate_college_reports"
        ])

    def test_chancellor_inherits_all_below(self):
        self.assertHasPermissions("CH", [
            "view_own_reports", "edit_own_reports", "delete_own_reports", "generate_own_reports",
            "view_department_reports", "generate_department_reports",
            "view_college_reports", "generate_college_reports",
            "can_view_university_reports", "can_generate_university_reports"
        ])

    def test_admin_does_not_inherit_anyone(self):
        self.assertHasPermissions("AD", [
            "add_departments", "add_colleges", "add_admins", "assign_roles", "remove_roles"
        ])
