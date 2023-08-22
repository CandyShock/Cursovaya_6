from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', blank=True)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', blank=True)

    is_active = models.BooleanField(default=False, verbose_name='Активирован')
    verification_key = models.CharField(max_length=20, default='Не верифицирован', verbose_name='Ключ Активации')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь сервиса'
        verbose_name_plural = 'Пользователи сервиса'
        ordering = ('pk',)

        permissions = [
            (
                'block_user', 'Block or unblock user'
            )
        ]
