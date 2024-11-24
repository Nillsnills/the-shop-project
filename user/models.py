from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("is_staff for superuser should be True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("is_superuser for superuser should be True")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    phone_number = models.CharField(unique=True, max_length=225)
    is_customer = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['phone_number', 'first_name', 'email']

    objects = UserManager()

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.username

