from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import IndexView

app_name = MailingConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]