import datetime
import math
# from datetime import datetime
from config.settings import CRONJOBS_PERIOD


def send_mail_now(mail) -> bool:

    print(datetime.datetime.now())
    recipients_list = [recipient.email_address for recipient in mail.addresses.all()]
    print(recipients_list)
    # try:
    #     sending_result = send_mail(
    #         subject=mail.message.subject,
    #         message=mail.message.text_message,
    #         from_email='xxx@yandexx.com',
    #         # from_email=settings.EMAIL_HOST_USER,
    #         recipient_list=recipients_list,
    #         fail_silently=False
    #     )
    # except Exception as err:
    #     server_response = err
    #     print(server_response)
    #     print(mail.message.subject)
    #     return False
    # else:
    #     server_response = 'OK'
    #     print(server_response)
    #     print(mail.message.subject)
    #     return True


def rounded_datetime(date_time: datetime):
    """
    Метод возвращает дату и время, с количеством минут, округленных до кратного
    параметру CRONJOBS_PERIOD. В большую сторону, начиная от начала часа.

    Например: если CRONJOBS_PERIOD=19, а date_time=2023-11-16 15:33:00, то
    метод вернет значение 2023-11-16 15:38:00. Или, если CRONJOBS_PERIOD=5,
    а date_time=2023-11-16 15:28:00, то метод вернет значение 2023-11-16 15:30:00.

    :param date_time: объект DateTime, который надо округлить
    :return: округленный объект DateTime
    """
    hours, minutes = divmod(math.ceil(date_time.minute / int(CRONJOBS_PERIOD)) * int(CRONJOBS_PERIOD), 60)
    return (date_time + datetime.timedelta(hours=hours)).replace(minute=minutes, second=0, microsecond=0)
