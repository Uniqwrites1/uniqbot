import json
import logging
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from .models import UserSession, MessageLog
from .bot_logic import WhatsAppBot

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def webhook(request):
    logger.info(f"Received {request.method} request to webhook")
    logger.info(f"GET params: {request.GET}")
    
    if request.method == "GET":
        return verify_webhook(request)
    elif request.method == "POST":
        return handle_webhook(request)
    
    return HttpResponseBadRequest("Method not allowed")

def verify_webhook(request):
    """Verify webhook with WhatsApp"""
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")
    
    logger.info(f"Webhook verification attempt - Mode: {mode}, Token: {token}, Challenge: {challenge}")
    logger.info(f"Expected token: {settings.WHATSAPP_VERIFY_TOKEN}")
    
    if mode and token:
        if mode == "subscribe" and token == settings.WHATSAPP_VERIFY_TOKEN:
            logger.info("Webhook verified successfully")
            return HttpResponse(challenge)
        else:
            logger.warning(f"Webhook verification failed. Expected token: {settings.WHATSAPP_VERIFY_TOKEN}, Received token: {token}")
            return HttpResponseBadRequest("Verification failed")
    
    # If no parameters, show helpful message instead of error
    if not any([mode, token, challenge]):
        return HttpResponse("Webhook endpoint is active. Use WhatsApp Business API to verify.")
    
    logger.warning("Missing parameters in webhook verification")
    return HttpResponseBadRequest("Missing parameters")

def handle_webhook(request):
    """Handle incoming WhatsApp messages"""
    try:
        data = json.loads(request.body)
        
        # Process webhook data
        if "entry" in data:
            for entry in data["entry"]:
                if "changes" in entry:
                    for change in entry["changes"]:
                        if change.get("field") == "messages":
                            process_message(change["value"])
        
        return HttpResponse("OK")
    
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return HttpResponseBadRequest("Error processing webhook")

def process_message(message_data):
    """Process incoming message and generate response"""
    try:
        logger.info(f"Processing message data: {json.dumps(message_data, indent=2)}")
        
        if "messages" in message_data:
            for message in message_data["messages"]:
                logger.info(f"Processing individual message: {json.dumps(message, indent=2)}")
                phone_number = message["from"]
                message_body = message.get("text", {}).get("body", "").strip()
                
                logger.info(f"Extracted phone: {phone_number}, message: {message_body}")
                
                # Log incoming message
                try:
                    MessageLog.objects.create(
                        phone_number=phone_number,
                        message_type="incoming",
                        message_content=message_body
                    )
                    logger.info("Incoming message logged successfully")
                except Exception as db_error:
                    logger.error(f"Error logging incoming message: {str(db_error)}")
                
                # Process with bot logic
                bot = WhatsAppBot()
                logger.info("Created WhatsAppBot instance")
                
                response = bot.process_message(phone_number, message_body)
                logger.info(f"Bot generated response: {response}")
                
                if response:
                    logger.info(f"Attempting to send message to {phone_number}")
                    send_result = bot.send_message(phone_number, response)
                    logger.info(f"Send message result: {send_result}")
                    
                    # Log outgoing message
                    try:
                        MessageLog.objects.create(
                            phone_number=phone_number,
                            message_type="outgoing",
                            message_content=response
                        )
                        logger.info("Outgoing message logged successfully")
                    except Exception as db_error:
                        logger.error(f"Error logging outgoing message: {str(db_error)}")
                else:
                    logger.warning("Bot did not generate a response")
    
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
