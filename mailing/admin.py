from django.contrib import admin

from mailing.models import Client, Message, Setting, Log


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'client_name', 'email', 'comment')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'subject_message', 'message')


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'mailing_time', 'frequency_mailing', 'mailing_status')


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'date_attempt', 'attempt_status', 'server_response')