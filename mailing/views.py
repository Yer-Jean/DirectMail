import random

from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView

from blog.models import Article
from mailing.models import Address, Message, Schedule, MailingLog
from users.models import User


class IndexView(generic.View):
# class IndexView(TemplateView):
    # template_name = 'mailing/index.html'

    def get(self, request):
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


class AddressListView(ListView):
    model = Address


class AddressCreateView(CreateView):
    model = Address
    fields = ('first_name', 'last_name', 'email_address', 'phone_number', 'gender', 'birthday', 'comment',)

    def get_success_url(self):
        return reverse('mailing:address_view', args=[self.object.pk])

    def form_valid(self, form):
        self.object = form.save()
        self.object.created_by = self.request.user
        self.object.save()

        return super().form_valid(form)


class AddressDetailView(DetailView):
    model = Address


class AddressUpdateView(UpdateView):
    model = Address
    fields = ('first_name', 'last_name', 'email_address', 'phone_number',
              'gender', 'birthday', 'comment', 'is_correct')

    def get_success_url(self):
        return reverse('mailing:address_view', args=[self.kwargs.get('pk')])


class AddressDeleteView(DeleteView):
    model = Address
    success_url = reverse_lazy('mailing:addresses')


class MessageListView(ListView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    fields = ('description', 'subject', 'text_message',)

    def get_success_url(self):
        return reverse('mailing:message_view', args=[self.object.pk])

    def form_valid(self, form):
        self.object = form.save()
        self.object.created_by = self.request.user
        self.object.save()

        return super().form_valid(form)


class MessageDetailView(DetailView):
    model = Message


class MessageUpdateView(UpdateView):
    model = Message
    fields = ('description', 'subject', 'text_message')

    def get_success_url(self):
        return reverse('mailing:message_view', args=[self.kwargs.get('pk')])


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:messages')


class ScheduleListView(ListView):
    model = Schedule


class ScheduleCreateView(CreateView):
    model = Schedule
    fields = '__all__'
    # fields = ('description', 'subject', 'text_message',)

    def get_success_url(self):
        # return reverse('mailing:schedule_view', args=[self.object.pk])
        return reverse('mailing:schedules')

    def form_valid(self, form):
        self.object = form.save()
        self.object.created_by = self.request.user
        self.object.save()

        return super().form_valid(form)


class ScheduleDetailView(DetailView):
    model = Schedule

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        schedule_item = Schedule.objects.get(pk=self.kwargs.get('pk'))
        address_item = Address.objects.filter(schedule=self.kwargs.get('pk'))
        # Можно вернуть только последнюю версию
        # if version_item:
        #     version_item = version_item.last()
        context_data['schedule_pk'] = schedule_item.pk
        context_data['address_item'] = address_item
        # context_data['title'] = f'{schedule_item.description}'

        return context_data


class ScheduleUpdateView(UpdateView):
    model = Schedule
    fields = '__all__'
    # fields = ('description', 'subject', 'text_message')

    def get_success_url(self):
        return reverse('mailing:schedule_view', args=[self.kwargs.get('pk')])


class ScheduleDeleteView(DeleteView):
    model = Schedule
    success_url = reverse_lazy('mailing:schedules')


class MailingLogListView(ListView):
    model = MailingLog


class MailingLogDetailView(DetailView):
    model = MailingLog
