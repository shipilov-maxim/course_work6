from django import forms
from django.forms import DateTimeInput

from distribution.models import Client, MailingSettings, Message


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.widgets.SelectMultiple):
                field.widget.attrs['class'] = 'form-control select2 select2-multiple'
            elif isinstance(field.widget, forms.widgets.Select):
                field.widget.attrs['class'] = 'form-control select2'
            elif isinstance(field, forms.DateTimeField):
                field.widget.attrs['class'] = 'form-control flatpickr-basic'
            elif isinstance(field.widget, forms.widgets.SelectMultiple):
                field.widget.attrs['class'] = 'form-control select2 select2-multiple'
            elif isinstance(field.widget, forms.widgets.Select):
                field.widget.attrs['class'] = 'form-control select2'
                # field.widget = DateTimeInput(
                #     attrs={'class': 'form-control flatpickr-basic',
                #            # "placeholder": "ДД.ММ.ГГГГ ЧЧ:ММ:СС",
                #            # "type": "datetime-local"
                #     }
                # )
            else:
                field.widget.attrs['class'] = 'form-control'


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


class MailingSettingsFormUpdate(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingSettings
        exclude = ('status', 'owner',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.DateTimeField):
                field.widget = DateTimeInput(
                    attrs={'class': 'form-control flatpickr-basic',
                           "placeholder": "ДД.ММ.ГГГГ ЧЧ:ММ:СС",
                           "type": "datetime"}
                )
