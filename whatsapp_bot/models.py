from django.db import models
from django.utils import timezone

class UserSession(models.Model):
    phone_number = models.CharField(max_length=20, unique=True)
    current_state = models.CharField(max_length=50, default='greeting')
    user_role = models.CharField(max_length=20, null=True, blank=True)
    last_intent = models.CharField(max_length=50, null=True, blank=True)  # Store detected intent
    intent_confidence = models.FloatField(null=True, blank=True)  # Store confidence score
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_sessions'

class MessageLog(models.Model):
    phone_number = models.CharField(max_length=20)
    message_type = models.CharField(max_length=20)  # incoming/outgoing
    message_content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'message_logs'
