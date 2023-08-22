from django.core.mail import send_mail

from config import settings
from mailing.models import Setting, Client, Log


def daily_send():
    for item in Setting.objects.filter(frequency_mailing='OPD'):
        if item.mailing_status in ('active', 'created'):
            item.save()
            send_newsletter(item)
            item.mailing_status = 'active'
            item.save()


def weekly_send():
    for item in Setting.objects.filter(frequency_mailing='OPW'):
        if item.mailing_status in ('active', 'created'):
            item.save()
            send_newsletter(item)
            item.mailing_status = 'active'
            item.save()


def monthly_send():
    for item in Setting.objects.filter(frequency_mailing='OPM'):
        if item.mailing_status in ('active', 'created'):
            item.save()
            send_newsletter(item)
            item.mailing_status = 'active'
            item.save()


def send_newsletter(object: Client):
    emails = [client.email for client in object.client.all()]
    try:
        send_mail(
            subject=object.message,
            message=object.message.message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=emails
        )
        attempt_status = 'success'
        server_response = 'Email sent successfully'
    except Exception as e:
        attempt_status = 'error'
        server_response = str(e)
    Log.objects.create(message=object.message,
                       attempt_status=attempt_status,
                       server_response=server_response)
