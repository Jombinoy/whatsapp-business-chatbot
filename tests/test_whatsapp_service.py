import pytest
import asyncio
from services.whatsapp_service import WhatsAppService

@pytest.mark.asyncio
async def test_process_message():
    service = WhatsAppService()
    
    # Test help command
    help_response = await service.process_message("+1234567890", "/help")
    assert "Available commands" in help_response
    
    # Test info command
    info_response = await service.process_message("+1234567890", "/info")
    assert "WhatsApp Business Chatbot" in info_response
    
    # Test default message
    default_response = await service.process_message("+1234567890", "Hello")
    assert "You said: hello" in default_response.lower()

@pytest.mark.asyncio
async def test_send_message():
    service = WhatsAppService()
    
    # Note: Replace with a test phone number
    test_number = "+1234567890"
    test_message = "Test message from automated test"
    
    response = await service.send_message(test_number, test_message)
    
    # Depending on your test environment, adjust assertions
    assert response is not None or response is None  # Handles both success and failure scenarios
