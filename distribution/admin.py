from django.contrib import admin

from distribution.models import Client, MailingLog, MailingSettings, Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'owner')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'id', 'surname', 'name', 'owner')


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'id', 'periodicity', 'status', 'message', 'owner')


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('time', 'id', 'status', 'server_response', 'mailing')
