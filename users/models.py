from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.

GENDER_CHOICE = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other')
)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Enter an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """
        - Overideing default django user model
    """
    username = None
    # setting up usename as None
    # Set the email field to unique
    email = models.EmailField(
        'email address', unique=True
    )
    mobile_no = models.IntegerField(
        "Mobile Number",
        null=True,
        blank=True
    )
    date_of_birth = models.DateField(
        "Date Of Birth",
        null=True,
        blank=True
    )
    gender = models.CharField(
        choices=GENDER_CHOICE,
        max_length=1,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email

class Hobbies(models.Model):
    """
        - save all hobbies
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class PersonalDetails(models.Model):
    """
        - Personal Details Of user
        - list of all hobies for perticuler user
        - age of user
    """
    user = models.OneToOneField(
        User,
        related_name="personal_detials",
        on_delete=models.CASCADE
    )
    hobbies = models.ManyToManyField(
        Hobbies,
        related_name="hobbies"
    )
    age = models.IntegerField()


    def __str__(self):
        return self.user.email