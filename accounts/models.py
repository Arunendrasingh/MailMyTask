from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, email, contact, password=None):
        """
        Creates and saves a User with the given email, contact and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        if not password:
            raise ValueError("Both Password must be same.")

        user = self.model(
            email=self.normalize_email(email),
            contact=contact,
            is_active=True
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, contact, password=None, password1=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """

        if not email:
            raise ValueError("Users must have an email address")

        if not password:
            raise ValueError("Both Password must be same.")

        user = self.create_user(
            email,
            password=password,
            contact=contact
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="Email Address",
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField(null=True, blank=True)
    contact = models.CharField(max_length=10)
    first_name = models.CharField(
        verbose_name="first name", max_length=150, blank=True)
    last_name = models.CharField(
        verbose_name="last name", max_length=150, blank=True)
    is_staff = models.BooleanField(
        verbose_name="staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        verbose_name="active",
        default=False,
        help_text="Designates whether this user should be treated as active. "
        "Unselect this instead of deleting accounts.",
    )
    is_superuser = models.BooleanField(
        verbose_name="Super User",
        default=False,
        help_text="Designates whether this user should be treated as SuperUser. "
        "Unselect this instead of deleting accounts.",
    )

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["contact"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_superuser

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return self.is_active and self.is_superuser

