from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import IndexView, AddressListView, AddressCreateView, AddressDetailView, AddressUpdateView, \
    AddressDeleteView, MessageListView, MessageCreateView, MessageDetailView, MessageUpdateView, MessageDeleteView

app_name = MailingConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('addresses/', AddressListView.as_view(), name='addresses'),
    path('addresses/create/', AddressCreateView.as_view(), name='address_create'),
    path('addresses/view/<int:pk>/', AddressDetailView.as_view(), name='address_view'),
    path('addresses/update/<int:pk>', AddressUpdateView.as_view(), name='address_update'),
    path('addresses/delete/<int:pk>', AddressDeleteView.as_view(), name='address_delete'),

    path('messages/', MessageListView.as_view(), name='messages'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/view/<int:pk>/', MessageDetailView.as_view(), name='message_view'),
    path('messages/update/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
    path('messages/delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),
]