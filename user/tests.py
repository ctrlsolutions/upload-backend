from django.test import TestCase
from user.models import Role, Permission, RolePermission

class RoleHierarchyTest(TestCase):
    def test_admin_inherits_manager_permissions(self):
        # Create roles
        admin_role = Role.objects.create(name="Admin", code="AD")
        manager_role = Role.objects.create(name="Manager", code="MG", parent=admin_role)

        # Create a permission
        view_permission = Permission.objects.create(name="Can view", code_name="can_view")

        # Assign permission to the Admin role
        RolePermission.objects.create(role=manager_role, permission=view_permission)

        # Assert Manager inherits Admin's permission
        self.assertTrue(view_permission in admin_role.get_permissions())

    def test_parent_inherits_child_permissions(self):
        # Create roles
        admin_role = Role.objects.create(name="Admin", code="AD")
        manager_role = Role.objects.create(name="Manager", code="MG", parent=admin_role)

        # Create permissions
        parent_perm = Permission.objects.create(name="Can delete", code_name="can_delete")
        child_perm = Permission.objects.create(name="Can edit", code_name="can_edit")

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
