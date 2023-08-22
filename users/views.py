import random

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import CreateView, UpdateView, TemplateView, ListView, DetailView

from users.forms import UserRegisterForm, RegisterForm, UpdateForm
from users.models import User


class UserView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'users.view_user'


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:notification')

    def form_valid(self, form):
        self.object = form.save()
        self.object.verification_key = ''.join([str(random.randint(0, 9))
                                                for _ in range(12)])

        send_mail(
            subject='Поздравляем c регистрацией',
            message=f'Для завершения регистрации пройдите по ссылке\n'
                    f'http://127.0.0.1:8000/users/verify/{self.object.verification_key}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.object.email]
        )
        return super().form_valid(form)


class ConfirmView(TemplateView):
    def get(self, *args, **kwargs):
        key = self.kwargs.get('key')
        user = User.objects.filter(verification_key=key).first()
        if user:
            user.is_active = True
            user.verification_key = key
            user.save()
            login(self.request, user)

        return redirect('users:reg_success')


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'


class ToggleAccountStatusView(PermissionRequiredMixin, generic.View):
    permission_required = 'users.block_user'

    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)
        if user.is_active:
            user.is_active = False
            send_deactivate_email(user)
        else:
            user.is_active = True
        user.save()
        return redirect(reverse('users:user_list'))


def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    send_mail(subject='Вы сменили пароль',
              message=f'Ваш новый пароль: {new_password}',
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[request.user.email]
              )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('main:prod_list'))
