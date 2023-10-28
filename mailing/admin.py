from django.contrib import admin

from mailing.models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email_address', 'phone_number',
                    'gender', 'birthday', 'comment', 'is_correct', 'created_date', 'modified_date')
    list_filter = ('created_date',)
