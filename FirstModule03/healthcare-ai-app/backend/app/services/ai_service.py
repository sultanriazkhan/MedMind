import openai
import json
from datetime import datetime
import os

class AIService:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.conversations = {}
    
    def stream_chat(self, message, user_id):
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        
        self.conversations[user_id].append({'role': 'user', 'content': message})
        
        messages = [
            {'role': 'system', 'content': 'You are a helpful medical AI assistant. Provide accurate, evidence-based health information. Do not give medical advice. Always recommend consulting healthcare professionals.'},
            *self.conversations[user_id][-10:]
        ]
        
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=messages,
            stream=True,
            temperature=0.7
        )
        
        full_response = ''
        for chunk in response:
            if chunk.choices[0].delta.get('content'):
                content = chunk.choices[0].delta.content
                full_response += content
                yield f"data: {json.dumps({'content': content})}\n\n"
        
        self.conversations[user_id].append({'role': 'assistant', 'content': full_response})
        yield "data: [DONE]\n\n"
    
    def stream_chat_with_context(self, message, context_data, user_id):
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        
        context_message = f"Based on the following lab report: {json.dumps(context_data)}\n\nUser question: {message}"
        self.conversations[user_id].append({'role': 'user', 'content': context_message})
        
        messages = [
            {'role': 'system', 'content': 'You are a medical AI assistant analyzing lab reports. Explain results in plain English, highlight abnormalities, and provide actionable insights.'},
            *self.conversations[user_id][-10:]
        ]
        
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=messages,
            stream=True,
            temperature=0.5
        )
        
        full_response = ''
        for chunk in response:
            if chunk.choices[0].delta.get('content'):
                content = chunk.choices[0].delta.content
                full_response += content
                yield f"data: {json.dumps({'content': content})}\n\n"
        
        self.conversations[user_id].append({'role': 'assistant', 'content': full_response})
        yield "data: [DONE]\n\n"
    
    def get_suggested_prompts(self, user_id):
        return [
            "What do my lab results mean?",
            "How can I improve my cholesterol levels?",
            "Explain my blood work in simple terms",
            "What lifestyle changes do you recommend?",
            "Should I be concerned about any results?"
        ]
    
    def clear_conversation(self, user_id):
        if user_id in self.conversations:
            del self.conversations[user_id]