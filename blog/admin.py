from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'content', 'picture', 'views', 'time_create')
