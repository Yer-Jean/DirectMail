import os

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Create a superuser with the specified email'

    def handle(self, *args, **options):
        superuser_email = os.getenv('SUPER_USER_EMAIL')
        # Проверка наличия суперпользователя с таким email
        if User.objects.get(email=superuser_email):
            self.stdout.write(self.style.ERROR(f'Superuser with email "{superuser_email}" already exists.'))
            return

        user = User.objects.create(
            email=os.getenv('SUPER_USER_EMAIL'),
            is_superuser=True,
            is_staff=True,
            is_active=True
        )
        user.set_password(os.getenv('SUPER_USER_PASSWORD'))
        user.save()
        self.stdout.write(self.style.SUCCESS(f'Superuser with email "{superuser_email}" successfully created.'))
