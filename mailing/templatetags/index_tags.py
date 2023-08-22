from random import sample
from blog.models import Blog
from mailing.models import *
from django import template

register = template.Library()


@register.simple_tag()
def total_mailing_number():
    return Setting.objects.count()


@register.simple_tag()
def active_mailing_number():
    return Setting.objects.filter(mailing_status='active').count()


@register.simple_tag()
def unique_customers_number():
    return Client.objects.distinct().count()


@register.filter()
def upload_media(image):
    if image:
        return f'/media/{image}'
    return '#'


@register.simple_tag()
def get_random_articles():
    articles = Blog.objects.all()

    if articles.count() >= 3:
        random_articles = sample(list(articles), 3)
    else:
        random_articles = articles

    return random_articles
