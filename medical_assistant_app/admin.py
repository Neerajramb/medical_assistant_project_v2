# medical_assistant_app/admin.py

from django.contrib import admin
from .models import ChatMessage

admin.site.register(ChatMessage)