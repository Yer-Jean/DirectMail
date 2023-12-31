# Generated by Django 4.2.6 on 2023-11-05 08:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mailing', '0003_message_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200, verbose_name='Description')),
                ('start_date', models.DateField(verbose_name='Start day')),
                ('end_date', models.DateField(verbose_name='End day')),
                ('periodic', models.CharField(choices=[('s', 'Single'), ('d', 'Daily'), ('w', 'Weekly'), ('m', 'Monthly')], max_length=1, verbose_name='Periodic')),
                ('time', models.TimeField(verbose_name='Mailing time')),
                ('day_of_week', models.CharField(blank=True, choices=[('mon', 'Monday'), ('tue', 'Tuesday'), ('wed', 'Wednesday'), ('thu', 'Thursday'), ('fri', 'Friday'), ('sat', 'Saturday'), ('sun', 'Sunday')], max_length=3, null=True, verbose_name='Day of the week')),
                ('day_of_month', models.IntegerField(blank=True, null=True, verbose_name='Day of the month')),
                ('status', models.CharField(choices=[('c', 'Created'), ('r', 'Started'), ('p', 'Paused'), ('e', 'Ended')], default='c', max_length=1, verbose_name='Status')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified date')),
                ('addresses', models.ManyToManyField(blank=True, to='mailing.address', verbose_name='Addresses')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.message', verbose_name='Message')),
            ],
            options={
                'verbose_name': 'Mailing',
                'verbose_name_plural': 'Mailing',
            },
        ),
    ]
