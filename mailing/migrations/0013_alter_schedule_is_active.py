# Generated by Django 4.2.6 on 2023-11-26 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0012_alter_schedule_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Active'),
        ),
    ]
