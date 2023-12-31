# Generated by Django 4.2.6 on 2023-11-25 06:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0011_schedule_is_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schedule',
            options={'ordering': ('-start_date',), 'permissions': [('set_active_status', 'Can activate/deactivate schedule')], 'verbose_name': 'Schedule', 'verbose_name_plural': 'Schedules'},
        ),
    ]
