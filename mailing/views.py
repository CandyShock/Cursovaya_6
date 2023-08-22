from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.forms import SettingForm, ClientForm, MessageForm, StyleFormMixin
from mailing.models import Setting, Log, Client, Message
from mailing.services import send_newsletter


class IndexView(generic.ListView):
    def get(self, request, *args, **kwargs):
        context = {
            'title': 'Главная',
        }
        return render(request, 'mailing/index.html', context)


class SettingListViews(LoginRequiredMixin, ListView):
    model = Setting
    permission_required = 'mailing.view_setting'

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user.pk)
        return queryset


class SettingDetailView(LoginRequiredMixin, DetailView):
    model = Setting
    template_name = 'mailing/setting_detail.html'


class SettingCreateView(LoginRequiredMixin, CreateView):
    model = Setting
    form_class = SettingForm
    template_name = 'mailing/setting_form.html'
    success_url = reverse_lazy('mailing:setting_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.mailing_status = 'created'
        self.object.save()
        if self.object.mailing_status in ('active', 'created'):
            send_newsletter(self.object)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class SettingUpdateView(LoginRequiredMixin, UpdateView):
    model = Setting
    form_class = SettingForm
    success_url = reverse_lazy('mailing:setting_list')
    permission_required = 'mailing.change_setting'


class SettingDeleteView(LoginRequiredMixin, DeleteView):
    model = Setting
    success_url = reverse_lazy('mailing:setting_list')
    template_name = 'mailing/setting_confirm_delete.html'


class SettingStatusMailing(PermissionRequiredMixin, generic.View):
    permission_required = 'mailing.block_status'

    def get(self, request, pk):

        setting = get_object_or_404(Setting, id=pk)
        if setting.mailing_status in ('created', 'active'):
            setting.mailing_status = 'closed'
        else:
            setting.mailing_status = 'created'

        setting.save()
        return redirect(reverse('mailing:setting_list'))


class LogListView(LoginRequiredMixin, ListView):
    model = Log


class LogDetailView(LoginRequiredMixin, DetailView):
    model = Log
    template_name = 'mailing/log_detail.html'


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user.pk)
        return queryset


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'mailing/client_detail.html'


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')
    template_name = 'mailing/client_confirm_delete.html'


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user.pk)
        return queryset


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')
    template_name = 'mailing/message_confirm_delete.html'
