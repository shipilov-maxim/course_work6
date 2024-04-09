from django.urls import path
from users.apps import UsersConfig
from users.views import LoginView, LogoutView, UserRegisterView, confirm_email, recover_password

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/', LogoutView.as_view(), name='profile'),
    path('confirm-register/<str:token>/', confirm_email, name='confirm_email'),
    path('recover_password/', recover_password, name='recover_password'),
]
