# chat/views.py
import os
from dotenv import load_dotenv
load_dotenv()
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Conversation, Message
from google import genai
from google.genai import types
from django.shortcuts import render, get_object_or_404

# Initialize the GenAI client using the hidden key
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def chat_page(request, conversation_id=None):
    if conversation_id is None:
        # Get or create a default conversation for visitors hitting '/'
        conversation, _ = Conversation.objects.get_or_create(id=1)
    else:
        conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # Notice we changed this to 'chat/index.html' to match your template
    return render(request, 'chat/chat.html', {'conversation': conversation})

@csrf_exempt 
def chat_api(request, conversation_id):
    if request.method == "POST":
        # 1. Properly parse the incoming JSON data from the JavaScript frontend
        try:
            data = json.loads(request.body)
            user_input = data.get("message")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid data format"}, status=400)
            
        # Ensure the user actually typed something
        if not user_input:
            return JsonResponse({"error": "Message cannot be empty"}, status=400)
        
        # 2. Get the current conversation or return a 404 if it doesn't exist
        conversation = get_object_or_404(Conversation, id=conversation_id)
        
        # 3. Retrieve the chat history from your SQL database
        past_messages = conversation.messages.all()
        
        # 4. Format history for the Gemini API
        formatted_history = []
        for msg in past_messages:
            formatted_history.append(
                types.Content(
                    role=msg.sender,
                    parts=[types.Part.from_text(text=msg.content)]
                )
            )
            
        # 5. Save the user's new message to the database
        Message.objects.create(
            conversation=conversation, 
            sender='user', 
            content=user_input
        )
            
        # 6. Initialize the chat session with the historical context
        chat = client.chats.create(
            model="gemini-3.5-flash", 
            config=types.GenerateContentConfig(
                system_instruction="You are a helpful AI assistant. Keep responses concise.",
            ),
            history=formatted_history
        )
        
        # 7. Send the new prompt to get the AI response
        response = chat.send_message(user_input)
        
        # 8. Save the AI's response to the database
        Message.objects.create(
            conversation=conversation, 
            sender='model', 
            content=response.text
        )
        
        # 9. Return the text back to the frontend
        return JsonResponse({"response": response.text})
