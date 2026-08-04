# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # This URL serves the HTML page for the user interface
    path('chat/<int:conversation_id>/', views.chat_page, name='chat_page'),

    # This URL receives the POST requests from the JavaScript code
    path('api/chat/<int:conversation_id>/', views.chat_api, name='chat_api'),
]