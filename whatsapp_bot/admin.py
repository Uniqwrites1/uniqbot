from django.contrib import admin
from .models import UserSession, MessageLog

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'user_role', 'current_state', 'created_at', 'updated_at']
    list_filter = ['user_role', 'current_state', 'created_at']
    search_fields = ['phone_number']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'message_type', 'timestamp', 'message_preview']
    list_filter = ['message_type', 'timestamp']
    search_fields = ['phone_number', 'message_content']
    readonly_fields = ['timestamp']
    
    def message_preview(self, obj):
        return obj.message_content[:50] + "..." if len(obj.message_content) > 50 else obj.message_content
    message_preview.short_description = "Message Preview"
