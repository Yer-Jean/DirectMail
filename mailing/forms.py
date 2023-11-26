from django import forms

from mailing.models import Address, Schedule, Message
from users.forms import StyleFormMixin


class AddressForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Address
        exclude = ('created_by',)


class MessageForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Message
        exclude = ('created_by',)


class ScheduleForm(forms.ModelForm):
    """Кастомная форма для заполнения расписания рассылки, так как при ее
    заполнении динамически меняются поля для ввода различных значений"""
    description = forms.CharField(widget=forms.TextInput())
    periodic = forms.ChoiceField(choices=Schedule.PERIODIC_CHOICES)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'dd/mm/yy'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'dd/mm/yy'}),
                               required=False)
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    day_of_week = forms.ChoiceField(choices=Schedule.DAY_OF_WEEK_CHOICES, required=False)
    day_of_month = forms.IntegerField(min_value=1, max_value=30, required=False)
    message = forms.ModelChoiceField(queryset=Message.objects.all(), empty_label=None)
    addresses = forms.ModelMultipleChoiceField(
        queryset=Address.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Передаем пользователя в форму через параметры
        super().__init__(*args, **kwargs)
        # Используем кастомный QuerySet для полей message и addresses
        if user:
            self.fields['message'].queryset = Message.objects.filter(created_by=user)
            self.fields['addresses'].queryset = Address.objects.filter(created_by=user)
        # Если форма открыта для редактирования, устанавливаем начальные значения
        if self.instance.pk:
            self.fields['message'].initial = self.instance.message
            self.fields['addresses'].initial = self.instance.addresses.all()
        #  Немного украсим форму - растянем поля ввода на всю ширину формы
        self.style_form_fields()

    class Meta:
        model = Schedule
        exclude = ('status', 'created_by',)

    def style_form_fields(self):
        for field_name, field in self.fields.items():
            if not isinstance(field, (forms.BooleanField, forms.ModelMultipleChoiceField)):
                field.widget.attrs['class'] = 'form-control'
