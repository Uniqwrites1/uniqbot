#!/usr/bin/env python3
"""
Production Validation Script - Smart WhatsApp Bot
This script validates that all smart bot features are working in production
"""

import os
import sys
import django

# Setup Django environment
sys.path.append('C:\\Dev\\python-django\\Uniqbot')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniqwrites.settings')
django.setup()

from whatsapp_bot.bot_logic import WhatsAppBot, SmartIntentRecognizer
from whatsapp_bot.models import UserSession
import requests

def validate_database_connection():
    """Test database connectivity and new fields"""
    print("📊 Validating Database Connection...")
    try:
        # Test database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # Test new fields
        session = UserSession.objects.create(
            phone_number="+validation_test",
            current_state="greeting", 
            last_intent="test_intent",
            intent_confidence=0.95
        )
        session.delete()  # Clean up
        print("✅ Database connection and new fields working!")
        return True
    except Exception as e:
        print(f"❌ Database validation failed: {str(e)}")
        return False

def validate_smart_intent_recognition():
    """Test the smart intent recognition system"""
    print("🧠 Validating Smart Intent Recognition...")
    try:
        recognizer = SmartIntentRecognizer()
        
        test_cases = [
            ("I need a math tutor", "tutoring_inquiry"),
            ("SAT exam preparation", "exam_prep"), 
            ("I want to volunteer", "volunteer_interest"),
            ("Tell me about literacy programs", "literacy_initiative"),
            ("What is PAP program", "pap_interest")
        ]
        
        passed = 0
        for message, expected_intent in test_cases:
            intent, confidence = recognizer.detect_intent(message)
            if intent == expected_intent and confidence > 0.3:
                passed += 1
                print(f"✅ '{message}' → {intent} ({confidence:.2f})")
            else:
                print(f"❌ '{message}' → {intent} ({confidence:.2f}) [Expected: {expected_intent}]")
        
        success_rate = (passed / len(test_cases)) * 100
        print(f"📊 Intent Recognition Success Rate: {success_rate:.1f}%")
        return success_rate > 80
        
    except Exception as e:
        print(f"❌ Intent recognition validation failed: {str(e)}")
        return False

def validate_bot_responses():
    """Test complete bot response system"""
    print("🤖 Validating Smart Bot Responses...")
    try:
        bot = WhatsAppBot()
        test_phone = "+production_test"
        
        # Clear any existing session
        UserSession.objects.filter(phone_number=test_phone).delete()
        
        test_messages = [
            "Hi there",
            "I need a physics tutor", 
            "parent",
            "My child needs homework help"
        ]
        
        responses = []
        for message in test_messages:
            response = bot.process_message(test_phone, message)
            responses.append(response[:100])
            print(f"✅ '{message}' → Response generated ({len(response)} chars)")
        
        # Clean up
        UserSession.objects.filter(phone_number=test_phone).delete()
        print("✅ Bot responses working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Bot response validation failed: {str(e)}")
        return False

def validate_production_environment():
    """Check production environment configuration"""
    print("🔧 Validating Production Environment...")
    try:
        from django.conf import settings
        import os
        
        checks = [
            ("WhatsApp Access Token", bool(settings.WHATSAPP_ACCESS_TOKEN)),
            ("WhatsApp Phone ID", bool(settings.WHATSAPP_PHONE_NUMBER_ID)), 
            ("Database URL", bool(os.environ.get('DATABASE_URL'))),
            ("Secret Key", bool(settings.SECRET_KEY))
        ]
        
        all_passed = True
        for check_name, result in checks:
            if result:
                print(f"✅ {check_name}: Configured")
            else:
                print(f"❌ {check_name}: Missing!")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Environment validation failed: {str(e)}")
        return False

def main():
    """Run all production validations"""
    print("🚀 PRODUCTION VALIDATION - Smart WhatsApp Bot")
    print("=" * 60)
    
    validations = [
        ("Database Connection", validate_database_connection),
        ("Smart Intent Recognition", validate_smart_intent_recognition), 
        ("Bot Response System", validate_bot_responses),
        ("Production Environment", validate_production_environment)
    ]
    
    results = []
    for name, validator in validations:
        print(f"\n{'='*20} {name} {'='*20}")
        result = validator()
        results.append((name, result))
        print("✅ PASSED" if result else "❌ FAILED")
    
    print(f"\n{'='*60}")
    print("🎯 VALIDATION SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{name:<25} {status}")
    
    print(f"\nOverall Success Rate: {passed}/{total} ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL VALIDATIONS PASSED!")
        print("🧠 Your smart WhatsApp bot is fully operational in production!")
        print("📱 Users can now chat naturally with AI-powered responses!")
        print("🚀 Ready to serve your educational platform customers!")
    else:
        print(f"\n⚠️  {total - passed} validation(s) failed.")
        print("Please check the errors above before going live.")

if __name__ == "__main__":
    main()
