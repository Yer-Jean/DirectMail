from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView

from mailing.models import Address


class IndexView(TemplateView):
    template_name = 'mailing/index.html'
    extra_context = {
        'title': 'DirectMail - HomePage',
        # 'navbar_template': 'mailing/includes/inc_navbar.html'
    }


class AddressListView(ListView):
    model = Address


class AddressCreateView(CreateView):
    model = Address
    # success_url = reverse_lazy('mailing:addresses')
    fields = ('first_name', 'last_name', 'email_address', 'phone_number', 'gender', 'birthday', 'comment',)
    extra_context = {
        'title': 'Dream shop - Blog',
        'sub_title': 'Add article',
        # 'navbar_template': 'address/includes/inc_navbar.html'
    }

    def get_success_url(self):
        return reverse('mailing:address_view', args=[self.object.pk])

    def form_valid(self, form):
        self.object = form.save()
        self.object.created_by = self.request.user
        self.object.save()

        return super().form_valid(form)


class AddressDetailView(DetailView):
    model = Address
    extra_context = {
        'title': 'Питомник - Главная',
        # 'navbar_template': 'address/includes/inc_navbar.html'
    }


class AddressUpdateView(UpdateView):
    model = Address
    fields = ('first_name', 'last_name', 'email_address', 'phone_number',
              'gender', 'birthday', 'comment', 'is_correct')
    extra_context = {
        'title': 'Dream shop - Blog',
        'sub_title': 'Edit article',
        # 'navbar_template': 'address/includes/inc_navbar.html'
    }

    def get_success_url(self):
        return reverse('mailing:address_view', args=[self.kwargs.get('pk')])


class AddressDeleteView(DeleteView):
    model = Address
    success_url = reverse_lazy('mailing:addresses')
    extra_context = {
        'title': 'Питомник - Главная',
        # 'navbar_template': 'address/includes/inc_navbar.html'
    }
