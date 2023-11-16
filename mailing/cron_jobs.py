from django.conf import settings
from django.core import management
from django.core.mail import send_mail


def send_scheduled_emails1():
    print('Cron working...')
    # send_mail(
    #     'This is the subject of test message',
    #     'This is the test message',
    #     settings.EMAIL_HOST_USER,
    #     ['yerg@mac.com']
    # )


def send_scheduled_emails():
    management.call_command('send_scheduled_emails')
