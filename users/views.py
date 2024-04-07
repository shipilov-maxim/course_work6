import secrets

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from users.forms import LoginForm, UserRegisterForm
from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'
    form_class = LoginForm


class LogoutView(BaseLogoutView):
    template_name = 'users/login.html'


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        token = secrets.token_hex(16)
        user = form.save()
        user.token = token
        host = self.request.get_host()
        link = f'http://{host}/users/confirm-register/{token}'
        message = f'Вы успешно зарегистрировались на нашем сайте! Подтвердите регистрацию по ссылке:\n{link}'
        send_mail('Подтвердите регистрацию', message, settings.EMAIL_HOST_USER, [user.email])
        return super().form_valid(form)


def confirm_email(token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('catalog:home'))


def recover_password(request):
    template_name = 'users/recover.html'

    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        new_password = secrets.token_hex(6)
        password = make_password(new_password)
        user.password = password
        user.save()
        message = f'Ваш временный пароль\n{new_password}'
        send_mail('Восстановление пароля', message, settings.EMAIL_HOST_USER, [user.email])
        return redirect(reverse('catalog:home'))
    return render(request, template_name)
