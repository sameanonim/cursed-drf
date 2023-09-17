from datetime import time

from django.conf import settings
from django.db import models


def default_start_time():
    return time(hour=0, minute=0)


def default_execution_time():
    return time(minute=2)


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='пользователь'
    )
    place = models.CharField(max_length=255, verbose_name='место')
    time = models.TimeField(default=default_start_time, verbose_name='время')
    action = models.CharField(max_length=255, verbose_name='действие')
    is_pleasurable = models.BooleanField(
        default=False,
        verbose_name='признак приятной привычки'
    )
    linked_habit = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='cвязанная привычка'
    )
    frequency = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='периодичность'
    )
    reward = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='вознаграждение'
    )
    execution_time = models.TimeField(
        default=default_execution_time,
        verbose_name='время на выполнение привычки'
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name='признак публичности привычки'
    )

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'

    def __str__(self):
        return f'{self.user} будет {self.action} в {self.time} в {self.place}'
