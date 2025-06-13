# medical_assistant_app/views.py

import json
from .llm_rag import get_rag_response, generate_follow_up_greeting
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
from .llm_rag import get_rag_response

# --- Page Rendering Views ---

@ensure_csrf_cookie
def auth_view(request):
    """Renders the login/signup page."""
    if request.user.is_authenticated:
        return redirect('chat_page')
    return render(request, 'auth.html')

@login_required
def chat_page_view(request):
    """Renders the main chat interface."""
    return render(request, 'chat.html')

@login_required
def logout_view(request):
    """Logs the user out and redirects to the auth page."""
    logout(request)
    return redirect('auth')

# --- API Views ---

@require_POST
def login_api(request):
    """API for user login."""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').lower()
        password = data.get('password')
        
        # Django's User model uses 'username', so we find the user by email first
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user:
            login(request, user)
            return JsonResponse({'success': True, 'message': 'Login successful!'})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid credentials. Please try again.'}, status=401)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

@require_POST
def signup_api(request):
    """API for user registration."""
    try:
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email', '').lower()
        password = data.get('password')

        if not all([name, email, password]):
            return JsonResponse({'success': False, 'error': 'All fields are required.'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'An account with this email already exists.'}, status=409)

        # We use email as the username for simplicity here
        if User.objects.filter(username=email).exists():
            return JsonResponse({'success': False, 'error': 'An account with this username already exists.'}, status=409)

        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.save()
        
        login(request, user)
        return JsonResponse({'success': True, 'message': 'Account created successfully!'}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

@login_required
def chat_history_api(request):
    """API to fetch ONLY the user's saved chat history."""
    messages = ChatMessage.objects.filter(user=request.user)
    history = list(messages.values('sender', 'message', 'timestamp'))
    return JsonResponse({'history': history})

# NEW: This view is dedicated to generating the welcome message.
@login_required
def welcome_message_api(request):
    """
    API to generate a dynamic, one-time welcome message.
    This message is NOT saved to the database.
    """
    # Check if there is any history to base a follow-up on
    last_user_message = ChatMessage.objects.filter(
        user=request.user, sender=ChatMessage.Sender.USER
    ).last()

    if last_user_message:
        # If history exists, ask the AI to generate a smart follow-up
        welcome_text = generate_follow_up_greeting(last_user_message.message)
    else:
        # Otherwise, use the generic greeting for a brand new user
        welcome_text = "Hello! I'm your personal medical assistant. How can I help you today?"

    return JsonResponse({'welcome_message': welcome_text})


@require_POST
@login_required
def chat_api(request):
    """API to handle a new chat message."""
    try:
        data = json.loads(request.body)
        user_message_text = data.get('message')

        if not user_message_text:
            return JsonResponse({'error': 'Message cannot be empty.'}, status=400)

        # Save user's message
        ChatMessage.objects.create(
            user=request.user, 
            sender=ChatMessage.Sender.USER, 
            message=user_message_text
        )

        # Fetch recent history for LLM context (e.g., last 10 messages)
        recent_messages = ChatMessage.objects.filter(user=request.user).order_by('-timestamp')[:10]
        conversation_history = [
            {'sender': msg.sender, 'message': msg.message} for msg in reversed(recent_messages)
        ]

        # Get response from the RAG system
        assistant_response_text = get_rag_response(user_message_text, conversation_history)

        # Save assistant's response
        ChatMessage.objects.create(
            user=request.user, 
            sender=ChatMessage.Sender.ASSISTANT, 
            message=assistant_response_text
        )

        return JsonResponse({'response': assistant_response_text})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    except Exception as e:
        print(f"Error in chat_api: {e}")
        return JsonResponse({'error': 'An internal server error occurred.'}, status=500)