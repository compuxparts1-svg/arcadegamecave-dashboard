#!/usr/bin/env python3
"""
Process and send queued email → Telegram messages
This runs as a background process and sends queued notifications
"""

import os
import json
import glob
import time
from pathlib import Path

QUEUE_DIR = "/tmp/email-telegram-queue"

def send_telegram_message(user_id, message):
    """Send message using OpenClaw sessions_send API"""
    try:
        import requests
        
        # Get gateway URL from environment or use default
        gateway_url = os.environ.get('OPENCLAW_GATEWAY_URL', 'http://localhost:7777')
        gateway_token = os.environ.get('OPENCLAW_GATEWAY_TOKEN', '')
        
        if not gateway_token:
            print(f"[SEND] No gateway token, cannot send")
            return False
        
        # Format message for Telegram
        payload = {
            "target": f"telegram:{user_id}",
            "message": message
        }
        
        headers = {
            "Authorization": f"Bearer {gateway_token}",
            "Content-Type": "application/json"
        }
        
        # Send via gateway message API
        response = requests.post(
            f"{gateway_url}/message/send",
            json=payload,
            headers=headers,
            timeout=5
        )
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"[SEND ERROR] {e}")
        return False

def process_queue():
    """Process all queued messages"""
    if not os.path.exists(QUEUE_DIR):
        return 0
    
    files = sorted(glob.glob(os.path.join(QUEUE_DIR, "msg-*.json")))
    
    if not files:
        return 0
    
    sent = 0
    for filepath in files:
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            user_id = data.get('userId')
            message = data.get('message')
            
            if not user_id or not message:
                os.remove(filepath)
                continue
            
            if send_telegram_message(user_id, message):
                os.remove(filepath)
                sent += 1
                print(f"[SENT] Removed: {os.path.basename(filepath)}")
            else:
                print(f"[RETRY] Keeping: {os.path.basename(filepath)}")
        
        except Exception as e:
            print(f"[ERROR] {filepath}: {e}")
    
    return sent

if __name__ == "__main__":
    sent = process_queue()
    if sent > 0:
        print(f"[DONE] Sent {sent} messages")
