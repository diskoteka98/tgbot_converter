from django.contrib import admin
from .models import User, Message, Currency, Rate
from simple_history.admin import SimpleHistoryAdmin


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('text', 'created_at')
    can_delete = False
    ordering = ['-created_at']


@admin.register(User)
class UserAdmin(SimpleHistoryAdmin):
    inlines = [MessageInline]
    list_display = ('telegram_id', 'username', 'message_count')
    search_fields = ('username', 'telegram_id')
    list_display_links = ['username', "telegram_id"]

    def message_count(self, obj):
        return obj.message_set.count()  # Возвращаем количество сообщений, связанных с пользователем

    message_count.short_description = 'Количество сообщений'  # Название колонки в списке пользователей


@admin.register(Message)
class MessageAdmin(SimpleHistoryAdmin):
    list_display = ('get_username', 'profile', 'text', 'created_at')
    search_fields = ('profile__username', 'text')
    list_display_links = ['profile', 'created_at']
    ordering = ['-created_at']
    list_per_page = 10
    list_filter = ('created_at', 'profile')

    def get_username(self, obj):
        return obj.profile.username if obj.profile else 'Неизвестный пользователь'

    get_username.short_description = 'Username'


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol')
    search_fields = ('name', 'symbol')


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ['currency_from', 'currency_to', 'rate', 'date']
    list_filter = ['currency_from', 'currency_to', 'date']
    search_fields = ['currency_from__name', 'currency_to__name']


