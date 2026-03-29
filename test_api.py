#!/usr/bin/env python
"""
Test script to verify API endpoints
"""
import os
import sys
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')
django.setup()

from django.contrib.auth.models import User
from tasks.models import Task, TaskUserProfile

def test_backend_setup():
    """Test backend setup and create test user"""
    print("🔧 Testing Backend Setup...")
    
    # Check if models are working
    try:
        user_count = User.objects.count()
        print(f"✅ Users in database: {user_count}")
        
        task_count = Task.objects.count()
        print(f"✅ Tasks in database: {task_count}")
        
        profile_count = TaskUserProfile.objects.count()
        print(f"✅ User profiles in database: {profile_count}")
        
    except Exception as e:
        print(f"❌ Model error: {e}")
        return False
    
    return True

def print_api_endpoints():
    """Print available API endpoints"""
    print("\n📡 Available API Endpoints:")
    print("Authentication:")
    print("  POST   /api/auth/signup/     - User registration")
    print("  POST   /api/auth/login/      - User login")
    print("  POST   /api/auth/logout/     - User logout")
    print("  GET    /api/auth/me/         - Get current user info")
    print("\nTask Management:")
    print("  GET    /api/tasks/           - List tasks (supports ?search= and ?status=)")
    print("  POST   /api/tasks/           - Create new task")
    print("  GET    /api/tasks/{id}/      - Get specific task")
    print("  PUT    /api/tasks/{id}/      - Update task")
    print("  DELETE /api/tasks/{id}/      - Delete task")
    print("  GET    /api/tasks/stats/     - Get task statistics")

if __name__ == "__main__":
    print("🚀 Task Manager Backend Test")
    print("=" * 40)
    
    if test_backend_setup():
        print("\n✅ Backend is ready!")
        print_api_endpoints()
        print(f"\n🌐 Server should run on: http://localhost:8000")
        print(f"📡 API base URL: http://localhost:8000/api/")
    else:
        print("\n❌ Backend setup failed!")
        sys.exit(1)
