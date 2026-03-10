#!/usr/bin/env python3
"""
AgentMail Webhook Handler
Receives emails from AgentMail and sends Telegram notifications

Usage:
  Set this as your AgentMail webhook endpoint in console.agentmail.to
  Then emails will automatically trigger Telegram alerts
"""

import os
import sys
import json
import subprocess
from datetime import datetime

TELEGRAM_USER_ID = "8627745904"

def log(msg):
    """Log with timestamp"""
    print(f"[{datetime.now().isoformat()}] {msg}")

def format_telegram_message(payload):
    """Format email as Telegram notification"""
    try:
        message = payload.get('message', {})
        sender = message.get('from_', message.get('from', 'Unknown'))
        subject = message.get('subject', '(no subject)')
        preview = message.get('extracted_text', message.get('text', ''))[:100]
        
        return f"📧 **New Email**\n\nFrom: {sender}\nSubject: {subject}\n\n_{preview}_"
    except Exception as e:
        log(f"Error formatting: {e}")
        return "📧 New email received"

def send_telegram_notification(message):
    """Send notification via OpenClaw message tool"""
    try:
        # Use OpenClaw's message command
        cmd = [
            'openclaw', 'message',
            'send',
            '--to', TELEGRAM_USER_ID,
            '--message', message
        ]
        
        log(f"Sending Telegram: {message[:50]}...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            log("✅ Telegram notification sent")
            return True
        else:
            log(f"❌ Telegram send failed: {result.stderr}")
            return False
            
    except Exception as e:
        log(f"Error sending notification: {e}")
        return False

def process_webhook(payload):
    """Process incoming AgentMail webhook"""
    try:
        event_type = payload.get('event_type')
        
        if event_type != 'message.received':
            log(f"Ignoring event type: {event_type}")
            return False
        
        log("📧 Email received!")
        
        message = payload.get('message', {})
        log(f"From: {message.get('from_', 'Unknown')}")
        log(f"Subject: {message.get('subject', '(no subject)')}")
        
        # Format and send Telegram notification
        telegram_msg = format_telegram_message(payload)
        success = send_telegram_notification(telegram_msg)
        
        return success
        
    except Exception as e:
        log(f"Error processing webhook: {e}")
        return False

def main():
    """For testing - read from stdin"""
    try:
        data = sys.stdin.read()
        payload = json.loads(data)
        
        log("Webhook received")
        log(f"Payload: {json.dumps(payload, indent=2)[:200]}...")
        
        process_webhook(payload)
        
    except json.JSONDecodeError as e:
        log(f"Invalid JSON: {e}")
        sys.exit(1)
    except Exception as e:
        log(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
