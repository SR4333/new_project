from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
#from django.utils.encoding import python_2_unicode_compatible


from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    middile_name = models.CharField(blank=True, max_length=50)
    role_type=models.CharField(max_length=50,default="user")


    def __str__(self):
        return self.email

