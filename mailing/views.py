import random

from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from blog.models import Article
from mailing.forms import ScheduleForm, MessageForm, AddressForm
from mailing.models import Address, Message, Schedule, MailingLog
from mailing.services import get_cache
from users.models import User


class GetQuerysetFromCacheMixin:

    def get_queryset(self):
        # Получаем результат запроса из кэша только тех записей, которые создал
        # текущий пользователь (если пользователь - staff, то показываем все записи)
        # Если данных в кэше нет, то запрашиваем в БД, используя фильтр, указанный в kwargs
        if self.request.user.role('managers'):
            kwargs = {}
        else:
            kwargs = {'created_by': self.request.user}
        queryset = get_cache(self.model, kwargs)
        return queryset


class IndexView(generic.View):

    @staticmethod
    def get(request):
        three_random_articles = []
        count_users = User.objects.all().count()
        count_schedules = Schedule.objects.all().count()
        count_active_schedules = Schedule.objects.filter(Q(status='c') | Q(status='r')).count()
        count_unique_addresses = Address.objects.all().distinct('email_address').count()

        # Выбираем три случайные статьи из блога (без повторов)
        all_published_articles = Article.objects.filter(is_published=True)
        num_of_published_articles = all_published_articles.count()
        while len(three_random_articles) < 3:
            i = random.randint(0, num_of_published_articles - 1)
            if all_published_articles[i] not in three_random_articles:
                three_random_articles.append(all_published_articles[i])

        # Формируем контекст для отображения на домашней странице
        context = {
            'count_users': count_users,
            'count_schedules': count_schedules,
            'count_active_schedules': count_active_schedules,
            'count_unique_addresses': count_unique_addresses,
            'object_list': three_random_articles,
        }
        return render(request, 'mailing/index.html', context)


class AddressListView(LoginRequiredMixin, GetQuerysetFromCacheMixin, ListView):
    model = Address


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm

    def get_success_url(self):
        return reverse('mailing:address_view', args=[self.object.pk])

    def form_valid(self, form):
        self.object = form.save()
        self.object.created_by = self.request.user
        self.object.save()
        return super().form_valid(form)


class AddressDetailView(LoginRequiredMixin, DetailView):
    model = Address


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = Address
    form_class = AddressForm

    def get_success_url(self):
        return reverse('mailing:address_view', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.created_by != self.request.user:
            raise Http404
        return self.object


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = Address
    success_url = reverse_lazy('mailing:addresses')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.created_by != self.request.user:
            raise Http404
        return self.object


class MessageListView(LoginRequiredMixin, GetQuerysetFromCacheMixin, ListView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse('mailing:message_view', args=[self.object.pk])

    def form_valid(self, form):
        self.object = form.save()
        self.object.created_by = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse('mailing:message_view', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.created_by != self.request.user:
            raise Http404
        return self.object


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:messages')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.created_by != self.request:
            raise Http404
        return self.object


class ScheduleListView(LoginRequiredMixin, GetQuerysetFromCacheMixin, ListView):
    model = Schedule


class ScheduleCreateView(LoginRequiredMixin, CreateView):
    model = Schedule
    form_class = ScheduleForm

    def get_success_url(self):
        return reverse('mailing:schedule_view', args=[self.object.pk])
        # return reverse('mailing:schedules')

    def form_valid(self, form):
        self.object = form.save()
        self.object.created_by = self.request.user
        self.object.is_active = True  # Присваиваю True вручную, так как вопреки описанию в модели Schedule
        #  значения данного поля по умолчанию default=True - при создании Schedule присваивается False
        self.object.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Передаем пользователя в форму
        return kwargs


class ScheduleDetailView(LoginRequiredMixin, DetailView):
    model = Schedule

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        schedule_item = Schedule.objects.get(pk=self.kwargs.get('pk'))
        address_item = Address.objects.filter(schedule=self.kwargs.get('pk'))
        context_data['schedule_pk'] = schedule_item.pk
        context_data['address_item'] = address_item

        return context_data


class ScheduleUpdateView(LoginRequiredMixin, UpdateView):
    model = Schedule
    form_class = ScheduleForm

    def get_success_url(self):
        return reverse('mailing:schedule_view', args=[self.kwargs.get('pk')])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.is_staff:
            kwargs['user'] = None
        else:
            kwargs['user'] = self.request.user  # Передаем пользователя в форму
        return kwargs

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.created_by != self.request.user or self.request.user.role('managers'):
            raise Http404
        return self.object


class ScheduleDeleteView(LoginRequiredMixin, DeleteView):
    model = Schedule
    success_url = reverse_lazy('mailing:schedules')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.created_by != self.request.user or self.request.user.role('managers'):
            raise Http404
        return self.object


@permission_required('mailing.set_schedule_active_status')
def toggle_active(request, pk):
    schedule = Schedule.objects.get(pk=pk)
    # Переключаем статус is_active, если только рассылка не завершена
    if schedule.status != 'f':
        schedule.is_active = {schedule.is_active: False,
                              not schedule.is_active: True}[True]
        schedule.save()
    else:
        messages.error(request, 'You cannot deactivate completed schedule')
    return redirect(reverse('mailing:schedules'))


@login_required
def toggle_run_pause(request, pk):
    schedule = Schedule.objects.get(pk=pk)
    # Переключаем статус running/pause, если только рассылка не завершена
    if schedule.status != 'f':
        schedule.status = {schedule.status == 'p': 'c',
                           schedule.status == 'c' or schedule.status == 'r': 'p'}[True]
        schedule.save()
    else:
        messages.error(request, 'You cannot run/pause completed schedule')
    return redirect(reverse('mailing:schedules'))


class MailingLogListView(LoginRequiredMixin, ListView):
    model = MailingLog

    def get_queryset(self):
        # Получаем логи из кэша только те, рассылки, которые создал
        # текущий пользователь (если пользователь - staff, то показываем все логи)
        # Если данных в кэше нет, то запрашиваем в БД, используя фильтр, указанный в kwargs
        if self.request.user.role('managers'):
            kwargs = {}
        else:
            kwargs = {'schedule__created_by': self.request.user}
        queryset = get_cache(self.model, kwargs)
        return queryset


class MailingLogDetailView(LoginRequiredMixin, DetailView):
    model = MailingLog
