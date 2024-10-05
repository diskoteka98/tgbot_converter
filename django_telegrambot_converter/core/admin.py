from django.contrib import admin
from .models import Profile
from .models import Message


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'name')
    search_fields = ('name', 'external_id')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'text', 'created_at')
    search_fields = ('username', 'text')
    list_filter = ('created_at',)


