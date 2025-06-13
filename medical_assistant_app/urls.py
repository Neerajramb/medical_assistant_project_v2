# medical_assistant_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # This line handles the root URL '/' and directs it to the auth page.
    path('', views.auth_view, name='auth'),

    path('chat/', views.chat_page_view, name='chat_page'),
    path('logout/', views.logout_view, name='logout'),

    # API endpoints
    path('api/login/', views.login_api, name='api_login'),
    path('api/signup/', views.signup_api, name='api_signup'),
    path('api/chat/', views.chat_api, name='api_chat'),
    path('api/history/', views.chat_history_api, name='api_chat_history'),
    path('api/welcome/', views.welcome_message_api, name='api_welcome'),
]