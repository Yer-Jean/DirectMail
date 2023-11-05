from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView

from mailing.models import Address, Message, Schedule


class IndexView(TemplateView):
    template_name = 'mailing/index.html'


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
        address_item = Address.objects.filter(schedule =self.kwargs.get('pk'))
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
