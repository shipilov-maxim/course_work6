from django import forms
from django.forms import DateTimeInput, SelectMultiple

from distribution.models import Client, MailingSettings, Message


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
            if isinstance(field, forms.DateTimeField):
                field.widget = DateTimeInput(
                    attrs={"placeholder": "ДД.ММ.ГГГГ ЧЧ:ММ:СС",
                           "type": "datetime-local"}
                )


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('owner',)


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('owner',)


class MailingSettingsForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = MailingSettings
        exclude = ('status', 'owner',)
