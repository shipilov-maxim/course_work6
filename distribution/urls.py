from django.urls import path

from distribution.apps import DistributionConfig
from distribution.views import (ClientCreateView, ClientDeleteView,
                                ClientDetailView, ClientListView,
                                ClientUpdateView, HomePageView,
                                MailingSettingsCreateView,
                                MailingSettingsDeleteView,
                                MailingSettingsListView,
                                MailingSettingsUpdateView, MessageCreateView,
                                MessageDeleteView, MessageDetailView,
                                MessageListView, MessageUpdateView,
                                set_timezone, MailingLogListView)

app_name = DistributionConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('create_message/', MessageCreateView.as_view(), name='create_message'),
    path('update_message/<int:pk>', MessageUpdateView.as_view(), name='update_message'),
    path('delete_message/<int:pk>', MessageDeleteView.as_view(), name='delete_message'),
    path('message/<int:pk>', MessageDetailView.as_view(), name='message'),
    path('messages', MessageListView.as_view(), name='messages'),
    path('create_client/', ClientCreateView.as_view(), name='create_client'),
    path('update_client/<int:pk>', ClientUpdateView.as_view(), name='update_client'),
    path('delete_client/<int:pk>', ClientDeleteView.as_view(), name='delete_client'),
    path('client/<int:pk>', ClientDetailView.as_view(), name='client'),
    path('clients', ClientListView.as_view(), name='clients'),
    path('create_distribution/', MailingSettingsCreateView.as_view(), name='create_distribution'),
    path('update_distribution/<int:pk>', MailingSettingsUpdateView.as_view(), name='update_distribution'),
    path('delete_distribution/<int:pk>', MailingSettingsDeleteView.as_view(), name='delete_distribution'),
    path('distributions', MailingSettingsListView.as_view(), name='distributions'),
    path('logs', MailingLogListView.as_view(), name='logs'),
    path('set_timezone', set_timezone, name='set_timezone')
]
