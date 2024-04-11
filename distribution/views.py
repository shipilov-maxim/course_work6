from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, DetailView
from distribution.forms import MessageForm, ClientForm, MailingSettingsForm
from distribution.models import Message, Client, MailingSettings
from django.shortcuts import redirect, render
import pytz
from django.utils import timezone
from distribution.services import apscheduler

scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
apscheduler(scheduler)


def set_timezone(request):
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        # form = UserCreateForm(request.POST)
        #
        # if form.is_valid():
        #     user = form.save(commit=False)
        #     user.username = request.POST.get('email')
        #     user.save()
        #
        #     return HttpResponseRedirect(reverse_lazy('homePage'))
        # return HttpResponse('Form not valid')
        # return reverse_lazy('distribution:home')
        return HttpResponseRedirect(reverse_lazy('distribution:home'))
    else:
        return render(request, 'distribution/includes/timezone.html', {'timezones': pytz.common_timezones})


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
        print(timezone.localtime(timezone.now()))
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('distribution:clients')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('distribution:clients')


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
