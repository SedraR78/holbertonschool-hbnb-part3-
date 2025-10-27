#!/usr/bin/env python3
import sys
import os

print("Testing with fixed models __init__.py...")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'hbnb'))

try:
    """ Import from models package"""
    from hbnb.app.models import User
    
    print("SUCCESS: User imported from models package")
    
    user = User("John", "Doe", "john@test.com")
    print(f"User created: {user.first_name} {user.last_name}")
    print(f"User ID: {user.id}")
    print(f"User email: {user.email}")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    
    """ Debug: check models/__init__.py content"""
    print("\nChecking models/__init__.py content...")
    try:
        with open("hbnb/app/models/__init__.py", "r") as f:
            content = f.read()
            print(f"models/__init__.py content:\n{content}")
    except Exception as e2:
        print(f"Cannot read models/__init__.py: {e2}")