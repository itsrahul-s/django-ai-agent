# chat/models.py
from django.db import models

class Conversation(models.Model):
    title = models.CharField(max_length=255, default="New Chat")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    # Link every message to a specific conversation
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    
    # Identify if the sender is the 'user' or the 'model'
    SENDER_CHOICES = (
        ('user', 'User'),
        ('model', 'Model'),
    )
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure messages are always loaded in chronological order
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender}: {self.content[:20]}..."