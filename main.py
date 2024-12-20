import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import uvicorn

from services.whatsapp_service import WhatsAppService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="WhatsApp Business Chatbot")

# Initialize WhatsApp Service
whatsapp_service = WhatsAppService()

class WebhookPayload(BaseModel):
    """Pydantic model for validating webhook payload"""
    object: str
    entry: list

@app.get("/webhook")
async def verify_webhook(hub_mode: str, hub_challenge: str, hub_verify_token: str):
    """
    Webhook verification endpoint for WhatsApp Business API
    """
    verify_token = os.getenv('WEBHOOK_VERIFY_TOKEN')
    
    if hub_mode == 'subscribe' and hub_verify_token == verify_token:
        logger.info("Webhook verified successfully")
        return int(hub_challenge)
    else:
        logger.warning("Webhook verification failed")
        raise HTTPException(status_code=403, detail="Verification failed")

@app.post("/webhook")
async def handle_webhook(payload: WebhookPayload):
    """
    Handle incoming WhatsApp messages
    """
    try:
        # Process each message in the payload
        for entry in payload.entry:
            for message_data in entry.get('changes', []):
                message = message_data.get('value', {}).get('messages', [{}])[0]
                
                # Extract message details
                from_number = message.get('from', '')
                message_body = message.get('text', {}).get('body', '')
                
                # Process and respond to the message
                response = await whatsapp_service.process_message(from_number, message_body)
                
                # Send response back
                await whatsapp_service.send_message(from_number, response)
        
        return {"status": "success"}
    
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/")
def read_root():
    """Simple health check endpoint"""
    return {"message": "WhatsApp Business Chatbot is running"}

@app.on_event("shutdown")
async def shutdown_event():
    """
    Cleanup resources on application shutdown
    """
    await whatsapp_service.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
