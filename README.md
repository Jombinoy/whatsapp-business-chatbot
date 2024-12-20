# WhatsApp Business Chatbot

## Overview
A modular WhatsApp Business Chatbot built with FastAPI and the official WhatsApp Business API, designed to handle incoming messages, provide dynamic responses, and serve as a flexible framework for future enhancements.

## Prerequisites
- Python 3.8+
- WhatsApp Business API Account
- Facebook Developer Account

## Setup Instructions

### 1. WhatsApp Business API Setup
1. Create a Facebook Developer Account
2. Set up a WhatsApp Business Account
3. Create a WhatsApp Business App
4. Obtain Access Token and Phone Number ID

### 2. Clone the Repository
```bash
git clone https://github.com/yourusername/whatsapp-chatbot.git
cd whatsapp-chatbot
```

### 3. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
1. Copy `.env.example` to `.env`
2. Fill in your WhatsApp Business API credentials:
   - `WHATSAPP_ACCESS_TOKEN`
   - `WHATSAPP_PHONE_NUMBER_ID`
   - `WHATSAPP_BUSINESS_ACCOUNT_ID`
   - `WEBHOOK_VERIFY_TOKEN`

### 6. Run the Application
```bash
uvicorn main:app --reload
```

### 7. Expose Local Server (Development)
Use ngrok to expose your local server:
```bash
ngrok http 8000
```

## Webhook Configuration
1. Go to Facebook Developer Console
2. Configure Webhook URL: `https://your-ngrok-url/webhook`
3. Set Webhook Verification Token
4. Subscribe to WhatsApp message events

## Features
- FastAPI-powered webhook
- Official WhatsApp Business API integration
- Async message processing
- Simple command handling
- Logging and error management

## Commands
- `/help`: Show available commands
- `/info`: Get bot information

## Future Enhancements
- Natural Language Processing
- Database integration
- Advanced message templates

## Troubleshooting
- Ensure WhatsApp Business API credentials are correct
- Check network connectivity
- Verify webhook configuration
- Monitor application logs

## Important Notes
- Keep your access token and credentials confidential
- Comply with WhatsApp Business API usage policies

## License
MIT License
