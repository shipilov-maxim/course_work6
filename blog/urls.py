from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogListView

app_name = BlogConfig.name

urlpatterns = [
    path('blogs', cache_page(60)(BlogListView.as_view()), name='blogs'),
]
