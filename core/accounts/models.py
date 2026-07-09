
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class Role(models.TextChoices):
    ADMINISTRATOR = 'administrator', 'Administrator'
    BURSAR        = 'bursar',        'Bursar'
    TEACHER       = 'teacher',       'Teacher'
    PARENT        = 'parent',         'Parent / Guardian'


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", Role.ADMINISTRATOR)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
   
    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email      = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)
    role       = models.CharField(max_length=20, choices=Role.choices, default=Role.TEACHER, db_index=True)

    
    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='users',
        db_index=True
    )

    phone_number = models.CharField(max_length=20, blank=True)
    home_address = models.TextField(blank=True)
    is_active    = models.BooleanField(default=True)
    is_staff     = models.BooleanField(default=False)  
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)


    objects = UserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'auth_user'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.full_name} <{self.email}> [{self.get_role_display()}]'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()


    # Convenience role checks 
  
    @property
    def is_administrator(self):
        return self.role == Role.ADMINISTRATOR

    @property
    def is_bursar(self):
        return self.role == Role.BURSAR

    @property
    def is_teacher(self):
        return self.role == Role.TEACHER

    @property
    def is_parent(self):
        return self.role == Role.PARENT
