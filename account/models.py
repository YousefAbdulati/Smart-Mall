from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        extra_fields.setdefault('is_admin', True)
        return self.create_user(email, name, password, **extra_fields)

# Custom User Model
class User(AbstractBaseUser):
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    ]
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='img', blank=True, null=True, default='')
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES, null=True, blank=True)
    nationality = models.CharField(max_length=255, default="Egypt")
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
