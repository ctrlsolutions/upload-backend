from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('The user must enter a valid email.')
        email = self.normalize_email(email)
        user_id = email.split('@')[0]
        kwargs.setdefault('user_id', user_id)
        user = self.model(user_id=user_id, email=email, **kwargs)
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



class CustomUser(AbstractBaseUser, PermissionsMixin):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say')
    ]

    ROLES = [
        ('CL', 'Clerk'),
        ('RE', 'Researcher'),
        ('FA', 'Faculty'),
        ('DH', 'Department Head'),
        ('CD', 'College Dean'),
        ('CH', 'Chancellor'),
        ('AD', 'Admin')
    ]

    user_id = models.CharField(max_length=255, unique=True, editable=False, primary_key=True)

    first_name = models.CharField(max_length=255, blank=True)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)

    sex = models.CharField(max_length=2, blank=True, choices=SEX_CHOICES)
    email = models.EmailField(unique=True)
    birthdate = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=3, choices=ROLES)
    google_id = models.CharField(max_length=255, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

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
        return self.role == role_code


    def __str__(self):
        return self.email


class BaseStaff(CustomUser):
    class Meta:
        proxy = True


class Faculty(CustomUser):
    class Meta:
        proxy = True


class DepartmentHead(Faculty):
    class Meta:
        proxy = True


class CollegeDean(DepartmentHead):
    class Meta:
        proxy = True


class Chancellor(CollegeDean):
    class Meta:
        proxy = True
