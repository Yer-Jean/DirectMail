from django.contrib import admin

from mailing.models import Address, Message, MailingLog, Schedule


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email_address', 'is_correct',
                    'created_by', 'created_date', 'modified_date')
    list_filter = ('created_date',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('description', 'subject', 'text_message', 'created_by', 'created_date', 'modified_date')
    list_filter = ('created_date',)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('description', 'start_date', 'end_date', 'periodic', 'time', 'day_of_week',
                    'day_of_month', 'message', 'status', 'created_by', 'created_date', 'modified_date')
    list_filter = ('start_date',)


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('date_of_last_attempt', 'status_of_last_attempt', 'server_response', 'message')
    list_filter = ('date_of_last_attempt',)
