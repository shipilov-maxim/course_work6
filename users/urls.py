from django.urls import path

from users.apps import UsersConfig
from users.views import (LoginView, LogoutView, UserRegisterView,
                         confirm_email, recover_password, UserListView, toggle_active)

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', UserListView.as_view(), name='users'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/', LogoutView.as_view(), name='profile'),
    path('confirm-register/<str:token>/', confirm_email, name='confirm_email'),
    path('recover_password/', recover_password, name='recover_password'),
    path('toggle_active_user/<int:pk>', toggle_active, name='toggle_active_user')
]
