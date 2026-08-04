from django.urls import path
from . import views

urlpatterns = [
    # Route for the main homepage '/'
    path('', views.chat_page, name='home'), 
    
    # Existing routes
    path('chat/<int:conversation_id>/', views.chat_page, name='chat_page'),
    path('api/chat/<int:conversation_id>/', views.chat_api, name='chat_api'),
]
