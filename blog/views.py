from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView
from blog.models import Blog
from distribution.views import BindOwnerMixin


class BlogListView(ListView):
    model = Blog
