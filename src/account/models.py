from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _t

FIRST_NAME_MAX_LENGTH = 100
LAST_NAME_MAX_LENGTH = 100 
EMAIL_MAX_LENGTH = 255
USERNAME_MAX_LENGTH = 100
USERNAME_MIN_LENGTH = 5
PASSWORD_MAX_LENGTH = 100
PASSWORD_MIN_LENGTH = 8

class CustomUser(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=USERNAME_MAX_LENGTH, unique=True)
    first_name = models.CharField(max_length=FIRST_NAME_MAX_LENGTH, verbose_name= _t('first name'))
    last_name = models.CharField(max_length=LAST_NAME_MAX_LENGTH, verbose_name= _t('last name'))
    email = models.EmailField(verbose_name= 'email address', unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_admin = models.BooleanField(default=False)
    objects = CustomUserManager()

    is_writer = models.BooleanField(default=False, verbose_name='User is a Writer') 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def __str__ (self) -> str:
        return self.email
