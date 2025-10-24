#!/usr/bin/env python3
"""Demo conversation through FastAPI server."""

from fastapi.testclient import TestClient
from app.main import app
import json

def simulate_conversation():
    """Simulate a conversation through the FastAPI server."""
    
    # Create test client
    client = TestClient(app)
    
    print('Starting conversation simulation through FastAPI server...')
    print('=' * 60)
    
    # Simulate a conversation with Asis
    conversation = [
        'My name is Asis. I am 34 years old, married with kids. I love sports, especially running and cycling.',
        'I need to prepare for the upcoming marathon in 3 months and also help my son with his cycling competition.',
        'When creating or updating ToDo items, focus on sports training schedules and family activities.',
        'I need to schedule my weekly long runs and find a good cycling route for weekend training.',
        'For the marathon training, I need to increase my weekly mileage gradually and add strength training.',
        'I need to register my son for the youth cycling championship and get his bike serviced.'
    ]
    
    user_id = 'Asis'
    session_id = 'demo-session-123'
    
    for i, message in enumerate(conversation, 1):
        print(f'\nMessage {i}: {message[:50]}...')
        
        # Send chat request
        response = client.post('/api/v1/chat', json={
            'message': message,
            'user_id': user_id,
            'session_id': session_id
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f'Response: {data["response"][:100]}...')
            print(f'   Session: {data["session_id"]}')
            print(f'   User: {data["user_id"]}')
        else:
            print(f'Error: {response.status_code} - {response.text}')
    
    print('\n' + '=' * 60)
    print('Conversation simulation complete!')
    
    # Check memory storage
    print('\nChecking stored memories...')
    
    # Get profile memories
    profile_response = client.get(f'/api/v1/memories/profile/{user_id}')
    if profile_response.status_code == 200:
        profile_data = profile_response.json()
        print(f'Profile memories: {len(profile_data["data"]["profiles"])} items')
        for profile in profile_data["data"]["profiles"]:
            print(f'   - {profile}')
    
    # Get todo memories
    todo_response = client.get(f'/api/v1/memories/todos/{user_id}')
    if todo_response.status_code == 200:
        todo_data = todo_response.json()
        print(f'Todo memories: {len(todo_data["data"]["todos"])} items')
        for todo in todo_data["data"]["todos"]:
            print(f'   - {todo}')
    
    # Get instruction memories
    instructions_response = client.get(f'/api/v1/memories/instructions/{user_id}')
    if instructions_response.status_code == 200:
        instructions_data = instructions_response.json()
        print(f'Instruction memories: {len(instructions_data["data"]["instructions"])} items')
        for instruction in instructions_data["data"]["instructions"]:
            print(f'   - {instruction}')
    
    print('\nMemory check complete!')

if __name__ == "__main__":
    simulate_conversation()
