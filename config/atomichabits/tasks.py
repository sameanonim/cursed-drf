from datetime import datetime, timedelta

import telebot
from celery import shared_task
from django.conf import settings


from atomichabits.models import Habit


@shared_task
def send_habit_reminders():
    bot = telebot.TeleBot(settings.TELEGRAM_BOT_API)
    time_now = datetime.now()
    start_time = time_now - timedelta(minutes=1)
    habit_data = Habit.objects.filter(time__gte=start_time)

    for habit in habit_data.filter(time__lte=time_now):
        message = f"{habit.user.login_tg}, пора {habit.action} в {habit.place}"
        bot.send_message(message, 'habit.user.chat_id')