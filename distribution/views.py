import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)
from distribution.forms import ClientForm, MailingSettingsForm, MessageForm
from distribution.models import Client, MailingSettings, Message, MailingLog
from distribution.services import apscheduler

scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)

# apscheduler(scheduler)


class BindOwnerMixin:

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            return self.model.objects.all().select_related("owner")
        else:
            return self.model.objects.filter(owner=self.request.user).select_related("owner")


class UpdateMixin:
    def get_form_class(self):
        user = self.request.user
        if user.groups.filter(name='менеджер').exists():
            return HttpResponseForbidden
        if user == self.object.owner or user.is_superuser:
            return self.form_class
        raise HttpResponseForbidden


class LimitedFormMixin:
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
            my_form_class = form_class(**self.get_form_kwargs())
            my_form_class["clients"].field.queryset = Client.objects.filter(owner=self.request.user)
            my_form_class["message"].field.queryset = Message.objects.filter(owner=self.request.user)
            return my_form_class


class HomePageView(TemplateView):
    template_name = "distribution/index.html"


class MessageCreateView(LoginRequiredMixin, BindOwnerMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('distribution:messages')


class MessageUpdateView(LoginRequiredMixin, BindOwnerMixin, UpdateMixin, UpdateView):
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


class ClientUpdateView(LoginRequiredMixin, BindOwnerMixin, UpdateMixin, UpdateView):
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


class MailingSettingsCreateView(LoginRequiredMixin, BindOwnerMixin, LimitedFormMixin, CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('distribution:distributions')


class MailingSettingsUpdateView(LoginRequiredMixin, BindOwnerMixin, LimitedFormMixin, UpdateMixin, UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('distribution:distributions')


class MailingSettingsDeleteView(LoginRequiredMixin, BindOwnerMixin, DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('distribution:distributions')


class MailingSettingsListView(LoginRequiredMixin, BindOwnerMixin, ListView):
    model = MailingSettings


class MailingLogListView(LoginRequiredMixin, BindOwnerMixin, ListView):
    model = MailingLog

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            return super().get_queryset().order_by('-time')
        else:
            return super().get_queryset().order_by('-time')


def set_timezone(request):
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        mailings: QuerySet = MailingSettings.objects.all()
        for mailing in mailings:
            mailing.start_time = timezone.localtime(mailing.start_time)
        return HttpResponseRedirect(reverse_lazy('distribution:home'))
    else:
        return render(request, 'distribution/timezone.html', {'timezones': pytz.common_timezones})


def toggle_active(request, pk):
    mailing = get_object_or_404(MailingSettings, pk=pk)
    if mailing.is_active:
        mailing.is_active = False
    else:
        mailing.is_active = True
    mailing.save()
    return redirect(reverse('distribution:distributions'))
