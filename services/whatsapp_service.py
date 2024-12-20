import os
import logging
import httpx
from typing import Optional, Dict, Any

class WhatsAppService:
    def __init__(self):
        """
        Initialize WhatsApp Business API client with credentials from environment variables
        """
        self.access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')
        self.phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
        self.business_account_id = os.getenv('WHATSAPP_BUSINESS_ACCOUNT_ID')
        
        # WhatsApp Business API base URL
        self.base_url = "https://graph.facebook.com/v19.0"
        
        # Configure logging
        self.logger = logging.getLogger(__name__)
        
        # Create an async HTTP client
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
        )
    
    async def process_message(self, from_number: str, message_body: str) -> str:
        """
        Process incoming messages and generate appropriate responses
        
        Args:
            from_number (str): Sender's phone number
            message_body (str): Content of the received message
        
        Returns:
            str: Response message to send back
        """
        # Convert message to lowercase for easier processing
        message_body = message_body.lower().strip()
        
        # Simple command and response handling
        if message_body == '/help':
            return "Available commands:\n/help - Show this help message\n/info - Get bot information"
        
        elif message_body == '/info':
            return "WhatsApp Business Chatbot\nVersion: 1.0\nCreated to demonstrate chatbot functionality"
        
        # Default response for unrecognized messages
        elif message_body:
            return f"You said: {message_body}. I'm a demo bot and can respond to /help and /info commands."
        
        return "Please send a valid message."
    
    async def send_message(self, to_number: str, message_body: str) -> Optional[Dict[str, Any]]:
        """
        Send a WhatsApp message using WhatsApp Business API
        
        Args:
            to_number (str): Recipient's phone number
            message_body (str): Message to send
        
        Returns:
            Optional[Dict[str, Any]]: Response from the API if sent successfully, None otherwise
        """
        try:
            # Validate input
            if not to_number or not message_body:
                self.logger.warning("Empty to_number or message_body")
                return None

            # Prepare message payload
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": to_number,
                "type": "text",
                "text": {"body": message_body}
            }
            
            # Send message endpoint
            url = f"{self.base_url}/{self.phone_number_id}/messages"
            
            # Send the message with timeout and error handling
            try:
                response = await self.client.post(
                    url, 
                    json=payload, 
                    timeout=10.0  # 10-second timeout
                )
            except httpx.RequestError as e:
                self.logger.error(f"Network error when sending message: {e}")
                return None
            except httpx.HTTPStatusError as e:
                self.logger.error(f"HTTP error when sending message: {e}")
                return None
            
            # Check response
            if response.status_code in [200, 201]:
                response_data = response.json()
                self.logger.info(f"Message sent successfully to {to_number}")
                return response_data
            else:
                self.logger.error(f"Failed to send message. Status: {response.status_code}, Response: {response.text}")
                return None
        
        except Exception as e:
            self.logger.error(f"Unexpected error in send_message: {e}")
            return None
    
    async def close(self):
        """
        Close the HTTP client session
        """
        await self.client.aclose()
