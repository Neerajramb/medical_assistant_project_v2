# medical_assistant_app/models.py

from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    class Sender(models.TextChoices):
        USER = 'user', 'User'
        ASSISTANT = 'assistant', 'Assistant'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    sender = models.CharField(max_length=10, choices=Sender.choices)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.sender} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['timestamp']