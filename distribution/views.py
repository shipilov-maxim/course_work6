from typing import Type, Union

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from distribution.forms import ClientForm, MailingSettingsForm, MessageForm
from distribution.models import Client, MailingSettings, Message, MailingLog
from distribution.services import apscheduler

scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
apscheduler(scheduler)

ModelsWithOwners = Type[Union[Client, Message, MailingSettings]]


class BindOwnerMixin:
    model: ModelsWithOwners

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            return self.model.objects.all().select_related("owner")
        else:
            return self.model.objects.filter(owner=self.request.user).select_related("owner")


def set_timezone(request):
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        mailings: QuerySet = MailingSettings.objects.all()
        for mailing in mailings:
            mailing.start_time = timezone.localtime(mailing.start_time)
        return HttpResponseRedirect(reverse_lazy('distribution:home'))
    else:
        return render(request, 'distribution/timezone.html', {'timezones': pytz.common_timezones})


class HomePageView(TemplateView):
    template_name = "distribution/index.html"


class MessageCreateView(LoginRequiredMixin, BindOwnerMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('distribution:messages')


class MessageUpdateView(LoginRequiredMixin, BindOwnerMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('distribution:messages')


class MessageDeleteView(LoginRequiredMixin, BindOwnerMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('distribution:messages')


class MessageDetailView(LoginRequiredMixin, BindOwnerMixin, DetailView):
    model = Message


class MessageListView(LoginRequiredMixin, BindOwnerMixin, ListView):
    model = Message


class ClientCreateView(LoginRequiredMixin, BindOwnerMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('distribution:clients')


class ClientUpdateView(LoginRequiredMixin, BindOwnerMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('distribution:clients')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('distribution:clients')


class ClientDetailView(LoginRequiredMixin, BindOwnerMixin, DetailView):
    model = Client


class ClientListView(LoginRequiredMixin, BindOwnerMixin, ListView):
    model = Client


class MailingSettingsCreateView(LoginRequiredMixin, BindOwnerMixin, CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('distribution:distributions')


class MailingSettingsUpdateView(LoginRequiredMixin, BindOwnerMixin, UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('distribution:distributions')


class MailingSettingsDeleteView(LoginRequiredMixin, BindOwnerMixin, DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('distribution:distributions')


class MailingSettingsListView(LoginRequiredMixin, BindOwnerMixin, ListView):
    model = MailingSettings


class MailingLogListView(LoginRequiredMixin, ListView):
    model = MailingLog
