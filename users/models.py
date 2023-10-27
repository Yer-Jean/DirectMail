from django.contrib.auth.models import AbstractUser
from django.db import models

from mailing.models import NULLABLE


class User(AbstractUser):
    username = None  # удаляем поле username, так как авторизовать будем по полю email
    email = models.EmailField(unique=True, verbose_name='Email')

    first_name = models.CharField(max_length=50, verbose_name='Name', **NULLABLE)
    last_name = models.CharField(max_length=50, verbose_name='Surname', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='Phone number', **NULLABLE)
    telegram = models.CharField(max_length=50, verbose_name='Telegram username', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Avatar', **NULLABLE)
    comment = models.TextField(verbose_name='Comment', **NULLABLE)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Created date')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Modified date')
    is_active = models.BooleanField(default=False, verbose_name='Active')
    verification_token = models.CharField(max_length=50, **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
