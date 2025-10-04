# users/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("The Username must be set")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)

        if not password:
            raise ValueError("Password must be provided")

        # обов’язково хешуємо пароль
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    # username вже є у AbstractUser
    email = models.EmailField(blank=True, null=True)

    # додаткові ролі
    is_student = models.BooleanField(default=True)
    is_admin_user = models.BooleanField(default=False)

    objects = CustomUserManager()

    def __str__(self):
        return self.username

