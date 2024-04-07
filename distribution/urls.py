from django.urls import path
from distribution.apps import DistributionConfig
from distribution.views import HomePageView

app_name = DistributionConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
]
