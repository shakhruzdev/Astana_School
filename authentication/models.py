from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

GENDER_CHOICES = [
    (1, "---"),
    (2, "MALE"),
    (3, "FEMALE"),
]


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("first_name", "Admin")
        extra_fields.setdefault("last_name", "User")
        extra_fields.setdefault("middle_name", "None")
        extra_fields.setdefault("birth_date", timezone.now().date())
        extra_fields.setdefault("gender", 1)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("teacher", "Teacher"),
        ("student", "Student"),
        ("admin", "Admin"),
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=1)
    birth_date = models.DateField(null=False)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grade = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - Grade: {self.grade}"


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    work_experience = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.subject}"
