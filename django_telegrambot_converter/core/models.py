from django.db import models


class Profile(models.Model):
    external_id = models.PositiveIntegerField(unique=True, verbose_name='ID пользователя в соц сети')
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Имя пользователя в соц сети')

    def __str__(self):
        return self.name or str(self.external_id)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Message(models.Model):
    user_id = models.PositiveIntegerField(null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username or 'Unknown'}: {self.text[:20]}"

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'