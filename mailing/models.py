from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Address(models.Model):
    GENDER = [
        ('m', 'male'),
        ('f', 'female'),
        ('u', 'unknown'),
    ]
    first_name = models.CharField(max_length=50, **NULLABLE, verbose_name='Name')
    last_name = models.CharField(max_length=50, **NULLABLE, verbose_name='Surname')
    email_address = models.EmailField(verbose_name='Email address')
    phone_number = models.CharField(max_length=20, **NULLABLE, verbose_name='Phone number')
    gender = models.CharField(max_length=7, choices=GENDER, default='u', verbose_name='Gender')
    birthday = models.DateField(**NULLABLE, verbose_name='Birthday')
    is_correct = models.BooleanField(default=True, verbose_name='Is correct')
    comment = models.TextField(**NULLABLE, verbose_name='Comment')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Created date')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Modified date')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   **NULLABLE, verbose_name='Created by')

    def __str__(self):
        return f'{self.email_address}: {self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'address'
        verbose_name_plural = 'addresses'
        ordering = ('email_address', 'last_name',)


class Message(models.Model):
    description = models.CharField(max_length=150, **NULLABLE, verbose_name='Description')
    subject = models.CharField(max_length=150, **NULLABLE, verbose_name='Subject')
    text_message = models.TextField(**NULLABLE, verbose_name='Message')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Created date')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Modified date')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   **NULLABLE, verbose_name='Created by')

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ('created_date',)
