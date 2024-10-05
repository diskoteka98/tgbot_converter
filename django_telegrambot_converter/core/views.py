from django.shortcuts import render
from django.http import JsonResponse
import telebot


def telegram_webhook(request):
    return JsonResponse({'status': 'ok'})