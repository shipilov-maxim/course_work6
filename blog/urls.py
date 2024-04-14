from django.urls import path
from blog.apps import BlogConfig
from blog.views import BlogListView

app_name = BlogConfig.name

urlpatterns = [
    path('blogs', BlogListView.as_view(), name='blogs'),
]
