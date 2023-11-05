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


class Schedule(models.Model):
    PERIODIC_CHOICES = (
        ('s', 'Single'),
        ('d', 'Daily'),
        ('w', 'Weekly'),
        ('m', 'Monthly'),
    )

    STATUS_CHOICES = (
        ('c', 'Created'),
        ('r', 'Started'),
        ('p', 'Paused'),
        ('e', 'Ended'),
    )

    DAY_OF_WEEK_CHOICES = (
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),
        ('sun', 'Sunday'),
    )

    description = models.CharField(max_length=200, verbose_name='Description')
    start_date = models.DateField(verbose_name='Start day')
    end_date = models.DateField(verbose_name='End day')
    periodic = models.CharField(max_length=1, choices=PERIODIC_CHOICES, verbose_name='Periodic')
    time = models.TimeField(verbose_name='Time to send')
    day_of_week = models.CharField(max_length=3, choices=DAY_OF_WEEK_CHOICES,
                                   verbose_name='Day of the week to send', **NULLABLE)
    day_of_month = models.IntegerField(verbose_name='Day of the month to send', **NULLABLE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Message')
    addresses = models.ManyToManyField(to=Address, blank=True, verbose_name='Addresses')
    status = models.CharField(default='c', max_length=1, choices=STATUS_CHOICES, verbose_name='Status')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Created date')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Modified date')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   **NULLABLE, verbose_name='Created by')

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Schedule'
        verbose_name_plural = 'Schedules'
