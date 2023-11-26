from datetime import datetime

from django.core.management import BaseCommand
from django.db.models import Q

from mailing.models import Schedule
from mailing.services import send_mail_now, rounded_datetime


class Command(BaseCommand):

    def handle(self, *args, **options):
        now = datetime.now()
        # Устанавливаем статус Completed(f) у устаревших ОДИНОЧНЫХ рассылок
        Schedule.objects.filter(~Q(status='f') & Q(periodic='s') & Q(start_date__lt=now)).update(status='f')
        # Устанавливаем статус Completed(f) у устаревших ПЕРИОДИЧЕСКИХ рассылок
        Schedule.objects.filter(~Q(status='f') & Q(end_date__lt=now)).update(status='f')

        # Устанавливаем статус Running(r) у рассылок, если наступила дата для их запуска
        Schedule.objects.filter(Q(status='c') & Q(start_date__lte=now)).update(status='r')

        # Выбираем все рассылки со статусом Running
        mailing = Schedule.objects.filter(status='r')

        for mail in mailing:
            this_mail_to_send = False  # Флаг отправки текущего письма
            from_db = rounded_datetime(datetime.combine(datetime.date(now), mail.time))
            from_now = rounded_datetime(now)
            # Если пришло время рассылки (для корректного сравнения округляем
            # текущее время и запланированное время рассылки):
            if from_db == from_now:
                # то проверяем настройки периодичности рассылки:
                match mail.periodic:
                    case 's' | 'd':
                        # Если пришло время высылать единичное или ежедневное письмо, то письмо будет выслано
                        this_mail_to_send = True
                    case 'w':
                        # Если пришло время высылать еженедельное письмо - проверяем день недели
                        # Если день недели запланирован в расписании рассылки, то письмо будет выслано
                        if mail.day_of_week == now.isoweekday():
                            this_mail_to_send = True
                    case 'm':
                        # Если пришло время высылать ежемесячное письмо - проверяем число месяца
                        # Если число месяца запланировано в расписании рассылки, то письмо будет выслано
                        if mail.day_of_month == now.day:
                            this_mail_to_send = True
                # Если письмо нужно высылать, то - высылаем
                if this_mail_to_send:
                    send_mail_now(mail)
