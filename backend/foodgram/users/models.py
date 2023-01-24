from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint

from .validators import username_validator


class User(AbstractUser):
    """ Класс Пользовотеля """
    email = models.EmailField(
        'Почта',
        max_length=settings.EMAIL_MAX_LENGTH,
        unique=True
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=settings.USERNAME_MAX_LENGTH,
        unique=True,
        validators=[username_validator]
    )
    first_name = models.CharField(
        'Имя',
        max_length=settings.FIRST_NAME_MAX_LENGTH
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=settings.LAST_NAME_MAX_LENGTH
    )
    password = models.CharField(
        'Пароль',
        max_length=settings.PASSWORD_MAX_LENGTH
    )

    class Meta:
        ordering = ('username',)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Follow(models.Model):
    """ Подписка на пользователя """
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    following = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписка',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            UniqueConstraint(
                fields=['user', 'following'],
                name='follow_unique'
            )
        ]

    def __str__(self):
        return f'{self.user.username} подписан на {self.following.username}'