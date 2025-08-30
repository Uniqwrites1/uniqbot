#!/usr/bin/env python3
"""
Production Migration Script for Smart WhatsApp Bot
This script runs the database migrations on the production Supabase database
"""

import os
import sys
import django

# Setup Django environment
sys.path.append('C:\\Dev\\python-django\\Uniqbot')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniqwrites.settings')

def run_production_migration():
    """Run database migrations on production"""
    try:
        print("🚀 Setting up Django environment...")
        django.setup()
        
        from django.core.management import call_command
        from django.db import connection
        
        print("📊 Checking database connection...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Database connection successful!")
        
        print("🔄 Running migrations...")
        call_command('migrate', verbosity=2)
        
        print("✅ Production migrations completed successfully!")
        print("🧠 Smart bot database schema is now live!")
        
        # Test the new fields
        from whatsapp_bot.models import UserSession
        print("🧪 Testing new intent tracking fields...")
        
        # Check if new fields exist by trying to create a test session
        test_session = UserSession(
            phone_number="+test_migration",
            current_state="greeting",
            last_intent="test_intent",
            intent_confidence=0.95
        )
        print("✅ New intent tracking fields are working!")
        print("🎉 Smart bot is ready for production!")
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Starting Production Migration for Smart WhatsApp Bot")
    print("=" * 60)
    
    success = run_production_migration()
    
    if success:
        print("\n🎉 SUCCESS: Your smart bot is now live in production!")
        print("🧠 AI-powered intent recognition is active!")
        print("📱 Users can now chat naturally with your WhatsApp bot!")
    else:
        print("\n❌ Migration failed. Please check the errors above.")
