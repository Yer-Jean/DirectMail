from django.conf import settings
from django.core.mail import send_mail


def send_scheduled_emails():
    print('Cron working...')
    # send_mail(
    #     'This is the subject of test message',
    #     'This is the test message',
    #     settings.EMAIL_HOST_USER,
    #     ['yerg@mac.com']
    # )
