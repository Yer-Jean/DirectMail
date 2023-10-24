from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'mailing/index.html'
    extra_context = {
        'title': 'DirectMail - HomePage',
        # 'navbar_template': 'mailing/includes/inc_navbar.html'
    }
