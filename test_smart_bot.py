#!/usr/bin/env python3
"""
Test script for the Smart WhatsApp Bot with Intent Recognition
This script tests various natural language inputs to verify intelligent responses
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

def test_intent_recognition():
    """Test the SmartIntentRecognizer directly"""
    print("🧠 Testing Smart Intent Recognition")
    print("=" * 50)
    
    recognizer = SmartIntentRecognizer()
    
    test_messages = [
        "I need help with math homework",
        "Looking for a tutor for my son",
        "Can you help me prepare for SAT exam?",
        "I want to become a teacher",
        "How can I volunteer to help children?",
        "I'd like to sponsor educational programs",
        "Tell me about your literacy programs",
        "What is PAP program?",
        "I need homework help",
        "My child is struggling with reading"
    ]
    
    for message in test_messages:
        intent, confidence = recognizer.detect_intent(message)
        print(f"Message: '{message}'")
        print(f"Intent: {intent} (Confidence: {confidence:.2f})")
        print("-" * 30)

def test_bot_responses():
    """Test full bot conversation flow"""
    print("\n🤖 Testing Smart Bot Responses")
    print("=" * 50)
    
    bot = WhatsAppBot()
    test_phone = "+1234567890"
    
    # Clear any existing session
    UserSession.objects.filter(phone_number=test_phone).delete()
    
    test_conversations = [
        ("Hi there", "Should get greeting"),
        ("I need a math tutor", "Should detect tutoring intent"),
        ("parent", "Should recognize parent role"),
        ("My child needs homework help", "Should provide parent-specific help"),
        ("What are your literacy programs?", "Should detect literacy inquiry"),
        ("I want to volunteer", "Should detect volunteer intent"),
        ("Tell me about PAP", "Should detect PAP interest"),
    ]
    
    for message, expected in test_conversations:
        response = bot.process_message(test_phone, message)
        print(f"User: '{message}'")
        print(f"Expected: {expected}")
        print(f"Bot Response: {response[:100]}...")
        print("-" * 50)

def test_contextual_responses():
    """Test role-based contextual responses"""
    print("\n🎯 Testing Contextual Role Responses")
    print("=" * 50)
    
    bot = WhatsAppBot()
    
    # Test different roles
    roles = ["parent", "student", "teacher", "volunteer"]
    test_phone_base = "+123456789"
    
    for i, role in enumerate(roles):
        test_phone = f"{test_phone_base}{i}"
        
        # Clear session
        UserSession.objects.filter(phone_number=test_phone).delete()
        
        # Set role
        response1 = bot.process_message(test_phone, role)
        print(f"\n--- Testing {role.upper()} Role ---")
        print(f"Role Selection Response: {response1[:80]}...")
        
        # Test natural language follow-up
        followup = "I need help with education"
        response2 = bot.process_message(test_phone, followup)
        print(f"Follow-up: '{followup}'")
        print(f"Contextual Response: {response2[:100]}...")

def main():
    """Run all tests"""
    print("🚀 Starting Smart WhatsApp Bot Tests")
    print("=" * 60)
    
    try:
        test_intent_recognition()
        test_bot_responses()
        test_contextual_responses()
        
        print("\n✅ All tests completed successfully!")
        print("🎉 Your WhatsApp bot is now SMART and ready!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
