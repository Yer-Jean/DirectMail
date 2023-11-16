from datetime import datetime, timedelta

from django.core.management import BaseCommand
from django.db.models import Q

from mailing.models import Schedule, MailingLog
from mailing.services import send_mail_now, rounded_datetime


class Command(BaseCommand):

    def handle(self, *args, **options):
        now = datetime.now()
        # Устанавливаем статус Completed у устаревших рассылок
        Schedule.objects.filter(~Q(status='f'), end_date__lt=now).update(status='f')

        # Устанавливаем статус Running у рассылок, если наступила дата для их запуска
        Schedule.objects.filter(Q(status='c'), start_date__lte=now).update(status='r')

        mailing = Schedule.objects.filter(status='r')
        # mailing = Schedule.objects.filter(Q(status='c') | Q(status='r'))

        for mail in mailing:
            mail_to_send = False
            from_db = rounded_datetime(datetime.combine(datetime.date(now), mail.time))
            from_now = rounded_datetime(now)
            self.stdout.write(self.style.SUCCESS(from_now))
            self.stdout.write(self.style.SUCCESS(from_db))
            # self.stdout.write(self.style.SUCCESS(now.day))
            # Если пришло время рассылки (для сравнения округляем текущее время и время рассылки)
            if from_db == from_now:
                # Ищем запись в логах о последней попытке отправки периодической рассылки
                last_mailing = MailingLog.objects.filter(message=mail.id).last()
                # self.stdout.write(self.style.SUCCESS(last_mailing))
                if not last_mailing:  # Если письмо ни разу не отправлялось, то отправляем согласно периодичности
                    match mail.periodic:
                        case 's' | 'd':
                            self.stdout.write(self.style.SUCCESS(mail.description))
                            mail_to_send = True
                        case 'w':
                            if mail.day_of_week == now.isoweekday():
                                self.stdout.write(self.style.SUCCESS(mail.description))
                                mail_to_send = True
                        case 'm':
                            if mail.day_of_month == now.day:
                                self.stdout.write(self.style.SUCCESS(mail.description))
                                mail_to_send = True
                else:
                    days_from_last_attempt = now.date() - last_mailing.date_of_last_attempt.date()
                    if (mail.periodic == 'm' and days_from_last_attempt == timedelta(days=30)
                            or mail.periodic == 'w' and days_from_last_attempt == timedelta(days=7)
                            or mail.periodic == 'd' and days_from_last_attempt == timedelta(days=1)):
                        mail_to_send = True

                if mail_to_send:
                    send_mail_now(mail)

        # send_mail(
        #     'This is the subject of test message',
        #     'This is the test message',
        #     settings.EMAIL_HOST_USER,
        #     ['yerg@mac.com']
        # )
        # print('This is Cron')
        # self.stdout.write(self.style.SUCCESS("Simple cron command successful"))
