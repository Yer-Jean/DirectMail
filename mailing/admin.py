from django.contrib import admin

from mailing.models import Address, Message


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email_address', 'is_correct',
                    'created_by', 'created_date', 'modified_date')
    list_filter = ('created_date',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('description', 'subject', 'text_message', 'created_by', 'created_date', 'modified_date')
    list_filter = ('created_date',)
