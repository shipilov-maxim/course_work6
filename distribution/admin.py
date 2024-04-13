from django.contrib import admin

from distribution.models import Client, MailingLog, MailingSettings, Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'id', 'surname', 'name')


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'id', 'periodicity', 'status', 'message')


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('time', 'id', 'status', 'server_response', 'mailing')
