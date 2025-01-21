from datetime import timezone

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import telebot
from telebot import types
import sqlite3
from django.db import models
from core.models import User
from core.models import Message
from core.converter import convert

import django


bot = telebot.TeleBot(settings.TELE_BOT_KEY)
name = None


@bot.message_handler(commands=["start"])
def start(message):
    user_data = message.from_user

    user, created = User.objects.get_or_create(
        telegram_id=user_data.id,
        defaults={
            'username': user_data.username
        }
    )

    if created:
        bot.reply_to(message, f"Привет, {user_data.first_name}! Ты был добавлен в базу данных.")
        bot.reply_to(message, f"{user_data.first_name}! Введи команду /converter для конвертации.")
    else:
        bot.reply_to(message, f"Привет снова, {user_data.first_name}! Введи команду /converter для конвертации.")

    Message.objects.create(
        profile=user,
        text=message.text,
    )


@bot.message_handler(commands=["converter"])
def go(message):
    bot.send_message(message.chat.id,  " Введите сумму")
    bot.register_next_step_handler(message, summa)


def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат. Впишите сумму")
        bot.register_next_step_handler(message, summa)
        return
    if amount > 0:
        markup1 = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton("USD/EUR", callback_data="usd/eur")
        btn2 = types.InlineKeyboardButton("EUR/USD", callback_data="eur/usd")
        btn3 = types.InlineKeyboardButton("USD/GBP", callback_data="usd/gbp")
        btn4 = types.InlineKeyboardButton("Другое значение", callback_data="else")
        markup1.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id,"Выберите пару валют", reply_markup=markup1)
    else:
        bot.send_message(message.chat.id, "Число должно быть больше 0. Впишите сумму")
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: call.data in ("usd/eur", "eur/usd", "usd/gbp","else"))
def callbacks(call):
    if call.data != "else":
        value = call.data.upper().split("/")
        res = convert(value[0], value[1], amount)
        bot.send_message(call.message.chat.id, f"Получается: {round(res, 2)}. Можете заново ввести сумму")
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, "Введите пару значений через слэш")
        bot.register_next_step_handler(call.message, my_currency)


def my_currency(message):
    try:
        value = message.text.upper().split("/")
        res = convert(value[0], value[1], amount)
        bot.send_message(message.chat.id, f"Получается: {round(res, 2)}. Можете заново ввести сумму")
        bot.register_next_step_handler(message, summa)

    except Exception:
        bot.send_message(message.chat.id, "Что-то не так. Впишите значение заново")
        bot.register_next_step_handler(message, my_currency)


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    try:
        user_telegram_id = message.from_user.id
        user = User.objects.get(telegram_id=user_telegram_id)
        text = message.text

        Message.objects.create(
            profile=user,
            text=message.text
        )
        bot.send_message(message.chat.id, "Ваше сообщение сохранено!")
    except django.db.utils.DatabaseError as db_error:
        bot.send_message(message.chat.id, "Ошибка базы данных при сохранении сообщения.")
        print(f"Ошибка базы данных: {db_error}")
    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка при сохранении сообщения.")
        print(f"Ошибка при сохранении сообщения: {e}")


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        print("start bot")
        bot.polling(non_stop=True)
