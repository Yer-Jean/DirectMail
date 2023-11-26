import random
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, UpdateView, ListView

from users.forms import UserForm, UserRegisterForm, LoginForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm  # Переопределяем стандартную форму UserCreationForm на свою
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        self.object = form.save()
        self.object.verification_token = get_random_string(30)
        send_mail(
            subject='Activate Your Account Now',
            message=f'Hello!\nPlease, click link below to confirm your email\n'
                    f'http://{get_current_site(self.request)}/users/confirm/{self.object.verification_token}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.object.email]
        )
        return super().form_valid(form)


def activate_user(request, token):
    user = User.objects.get(verification_token=token)
    user.verification_token = ''
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserForm

    # переопределяем этот метод для того, чтобы не передавать в URL номер редактируемого объекта (pk)
    # то есть редактировать будем всегда текущего пользователя, под которым зашли на платформу
    def get_object(self, queryset=None):
        return self.request.user


class UserLoginView(LoginView):
    model = User
    form_class = LoginForm


class UserListView(LoginRequiredMixin, ListView):
    model = User


@permission_required('users.set_user_active_status')
def toggle_active(request, pk):
    user = User.objects.get(pk=pk)
    # Переключаем статус is_active, если только это не текущий пользователь
    if user.email != request.user.email and not user.is_superuser and not user.is_staff:
        user.is_active = {user.is_active: False,
                          not user.is_active: True}[True]
        user.save()
    else:
        messages.error(request, 'You cannot deactivate this user')
    return redirect(reverse('users:users'))


def password_reset(request):

    if request.method == 'POST':
        # Проверка на существование введенного email в БД
        try:
            user = User.objects.get(email=request.POST.get('email'))
        except User.DoesNotExist:
            messages.error(request, 'Entered email not found')
            return render(request, 'users/password_reset.html')
        # Генерируем пароль из 12-ти случайных цифр
        new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
        # Отправляем пароль по email пользователю
        send_mail(
            subject='New password',
            message=f'Hello!\nThis is your new password: {new_password}\n\nDo not tell it to anyone.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        # Записываем в БД новый пароль
        user.set_password(new_password)
        user.save()
        # После отправки письма с паролем переходим на страницу авторизации
        return redirect(reverse_lazy('users:login'))
    return render(request, 'users/password_reset.html')
