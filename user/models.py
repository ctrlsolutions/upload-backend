from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('The user must enter a valid email.')
        email = self.normalize_email(email)
        username = email.split('@')[0]
        user = self.model(email=email, username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **kwargs)
    
class Permission(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code_name = models.CharField(max_length=255, unique=True)

class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name="children" )

    def has_permission(self, permission_code):
        return permission_code in [perm.code_name for perm in self.get_permissions()]
        
    def get_permissions(self):
        """Top down approach"""
        permissions = set(self.permissions.all())
        for child in self.children.all():
            permissions.update(child.get_permissions())
        return permissions

    
    permissions = models.ManyToManyField(
    Permission,
    through='RolePermission',
    through_fields=('role', 'permission'),
    related_name='roles'
)
    def __str__(self):
        return self.name


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say')
    ]

    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)

    first_name = models.CharField(max_length=255, blank=True)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)

    sex = models.CharField(max_length=2, blank=True, choices=SEX_CHOICES)
    email = models.EmailField(unique=True)
    birthdate = models.DateField(null=True, blank=True)

    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    google_id = models.CharField(max_length=255, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Add ForeignKey to Department
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    college = models.ForeignKey('College', on_delete=models.SET_NULL, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_set",
        blank=True
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def has_role(self, role_code):
        return self.role.code == role_code
    
    def has_permission(self, permission_codename):
        return self.role and self.role.has_permission(permission_codename)

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        # Combine first and last name, with middle name if it exists
        full_name = f"{self.first_name} {self.middle_name[:1] + '. ' if self.middle_name else ''}{self.last_name}"
        return full_name

class College(models.Model):
    college_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name="departments")

    def __str__(self):
        return f"{self.name} ({self.college.code})"
