from datetime import datetime, timedelta
from math import ceil

from django.core.cache import cache
from django.conf import settings
from django.core.mail import send_mail

from config.settings import CRONJOBS_PERIOD
from mailing.models import MailingLog


def send_mail_now(mail) -> bool:

    print(datetime.now())
    recipients_list = [recipient.email_address for recipient in mail.addresses.all()]
    print(recipients_list)
    try:
        send_mail(
            subject=mail.message.subject,
            message=mail.message.text_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipients_list,
            fail_silently=False,
        )
    except Exception as err:
        MailingLog.objects.create(
            status_of_last_attempt=False,
            server_response=err,
            schedule=mail,
        )
        print(mail.message.subject)
        return False
    else:
        MailingLog.objects.create(
            status_of_last_attempt=True,
            server_response='Message sent successfully',
            schedule=mail,
        )
        return True


def rounded_datetime(date_time: datetime):
    """
    Метод возвращает дату и время, с количеством минут, округленных до кратного
    параметру CRONJOBS_PERIOD. В большую сторону, начиная от начала часа.

    Например: если CRONJOBS_PERIOD=19, а date_time=2023-10-16 15:33:00, то
    метод вернет значение 2023-10-16 15:38:00,
    или,
    если CRONJOBS_PERIOD=5, а date_time=2023-10-16 15:28:00, то
    метод вернет значение 2023-10-16 15:30:00.

    :param date_time: объект DateTime, который надо округлить
    :return: округленный объект DateTime
    """
    hours, minutes = divmod(ceil(date_time.minute / int(CRONJOBS_PERIOD)) * int(CRONJOBS_PERIOD), 60)
    return (date_time + timedelta(hours=hours)).replace(minute=minutes, second=0, microsecond=0)


def get_cache(model, kwargs):
    if settings.CACHE_ENABLE:
        key = f'{model.__name__}_list'
        cache_list = cache.get(key)
        print(kwargs)
        if cache_list is None:
            cache_list = model.objects.filter(**kwargs)
            cache.set(key, cache_list)
    else:
        cache_list = model.objects.filter(**kwargs)
    return cache_list
