import secrets
from users.models import User
from django.views.generic import CreateView
from users.forms import UserRegForm
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView


class UserCreateView(CreateView):
    model = User
    form_class = UserRegForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Добрый день! Для подтверждения регистрации по почте перейдите по ссылке: {url} ",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class NewPasswordView(PasswordResetView):
    form_class = PasswordResetForm
    template_name = "users/reset_password.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user = User.objects.get(email=email)
        if user:
            password = secrets.token_urlsafe(10)
            send_mail(
                subject="Новый пароль",
                message=f"Здравствуйте! Новый пароль для входа в аккаунт: {password}",
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
            user.set_password(password)
            user.save()

            return redirect(reverse("users:login"))

        else:
            return redirect(reverse("users/reset_password.html"))
