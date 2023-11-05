# Generated by Django 4.2.6 on 2023-11-05 08:55

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mailing', '0004_mailinglist'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MailingList',
            new_name='Schedule',
        ),
        migrations.AlterModelOptions(
            name='schedule',
            options={'verbose_name': 'Schedule', 'verbose_name_plural': 'Schedules'},
        ),
    ]
