import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
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


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('distribution:messages')

    def form_valid(self, form):
        self.object = form.save()
        self.object.creator = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('distribution:messages')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('distribution:messages')


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageListView(LoginRequiredMixin, ListView):
    model = Message


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('distribution:clients')

    def form_valid(self, form):
        self.object = form.save()
        self.object.creator = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('distribution:clients')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('distribution:clients')


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientListView(LoginRequiredMixin, ListView):
    model = Client


class MailingSettingsCreateView(LoginRequiredMixin, CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('distribution:distributions')

    def form_valid(self, form):
        self.object = form.save()
        self.object.creator = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailingSettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('distribution:distributions')


class MailingSettingsDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('distribution:distributions')


class MailingSettingsListView(ListView):
    model = MailingSettings


class MailingLogListView(ListView):
    model = MailingLog
