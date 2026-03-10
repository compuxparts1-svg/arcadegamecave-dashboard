# Email Webhook Setup Guide

## Overview

This document explains how to complete the AgentMail → Telegram notification system setup so you receive **instant alerts when emails arrive**.

## Current Status

✅ **What's already running:**
- Webhook server listening on `localhost:3000`
- Email parser ready
- Telegram formatter ready
- Git backups complete

⏳ **What needs to be done:**
- Configure AgentMail to send webhooks to your public endpoint
- Test the end-to-end flow

---

## Step 1: Expose the Webhook Server to the Internet

Your webhook server is running locally on port 3000, but AgentMail needs a **public URL** to send webhooks to.

### Option A: Use ngrok (Already Configured)

You already have ngrok set up at:
```
https://unimposed-hyman-cognoscitively.ngrok-free.dev/agentmail
```

But the actual webhook server is on **port 3000**, so you need to update this URL.

**Check what's currently pointing to port 3000:**
```bash
# Test if webhook server responds
curl http://localhost:3000/

# You should see:
# {
#   "status": "running",
#   "uptime": ...,
#   "emailsProcessed": ...
# }
```

### Option B: Update ngrok Tunnel (If Needed)

If your ngrok tunnel isn't pointing to port 3000:

```bash
# Install ngrok (if not already installed)
# https://ngrok.com/download

# Start ngrok tunnel to port 3000
ngrok http 3000
```

This will give you a public URL like:
```
https://abc123def456.ngrok.io
```

---

## Step 2: Configure AgentMail Webhook

1. **Go to AgentMail Console:**
   - https://console.agentmail.to
   - Log in with your account

2. **Navigate to Webhooks:**
   - Click **"Dashboard"** → **"Webhooks"** in sidebar
   - Or direct URL: https://console.agentmail.to/dashboard/webhooks

3. **Update/Add Webhook Endpoint:**
   - Find the existing endpoint: `https://unimposed-hyman-cognoscitively.ngrok-free.dev/agentmail`
   - Or add a new one if missing
   - **Change URL to:**
     ```
     https://unimposed-hyman-cognoscitively.ngrok-free.dev/webhook
     ```
     (or your actual ngrok URL + `/webhook`)

4. **Save & Test:**
   - AgentMail should confirm the webhook is active
   - You'll see in the Logs tab that it's sending to your endpoint

---

## Step 3: Test End-to-End

### Test 1: Manual Webhook Test

```bash
# Send a test webhook to your server
curl -X POST http://localhost:3000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "message.received",
    "message": {
      "from_": "Test Sender <test@example.com>",
      "subject": "Test Email",
      "text": "If you got a Telegram notification, it works!",
      "timestamp": "2026-03-06T00:00:00.000Z"
    }
  }'
```

**Expected response:**
```json
{
  "success": true,
  "emailCount": 1,
  "notificationSent": true,
  "message": "Email processed and Telegram notification sent"
}
```

**Check logs:**
```bash
tail -10 /tmp/email-webhook.log
```

You should see:
```
[..../...] 📧 EMAIL #X
From: Test Sender <test@example.com>
Subject: Test Email
Notification: 📧 **New Email** ...
[TELEGRAM] ✅ Notification sent
```

### Test 2: Real AgentMail Email

1. **Send an email** to `arcadegamecave@agentmail.to` from your personal email
2. **Watch the logs:**
   ```bash
   tail -f /tmp/email-webhook.log
   ```
3. **Check Telegram** - you should get a notification:
   ```
   📧 **New Email**
   
   From: Your Name <your.email@example.com>
   Subject: Your subject line
   
   _Your message preview..._
   ```

---

## Managing the Webhook Server

### Start the server
```bash
bash /home/jason/.openclaw/workspace/start-email-webhook.sh
```

**Output:**
```
✅ Email webhook server started (PID: 12345)
   Log file: /tmp/email-webhook.log
   To stop: kill 12345
```

### Stop the server
```bash
bash /home/jason/.openclaw/workspace/stop-email-webhook.sh
```

### View logs in real-time
```bash
tail -f /tmp/email-webhook.log
```

### Check if server is running
```bash
ps aux | grep "email-webhook-server" | grep -v grep
```

---

## Webhook Payload Format

When an email arrives, AgentMail sends this JSON structure:

```json
{
  "event_type": "message.received",
  "message": {
    "from_": "Name <email@domain.com>",
    "subject": "Email subject",
    "text": "Plain text body",
    "extracted_text": "Cleaned up body",
    "timestamp": "2026-03-06T06:00:00.000Z",
    "inbox_id": "arcadegamecave@agentmail.to",
    "thread_id": "thread-abc123",
    "message_id": "<msg-123@mail.com>"
  }
}
```

The webhook server:
1. ✅ Parses `from_` to extract sender name and email
2. ✅ Extracts subject and message preview
3. ✅ Formats as Telegram notification
4. ✅ Sends to your Telegram account

---

## Troubleshooting

### Problem: Webhook not firing when emails arrive

**Check:**
1. Is the server running?
   ```bash
   ps aux | grep email-webhook-server
   ```

2. Is the AgentMail webhook URL correct?
   - Go to https://console.agentmail.to/dashboard/webhooks
   - Verify the endpoint URL matches your ngrok tunnel

3. Is ngrok tunnel still active?
   ```bash
   curl https://your-ngrok-url.ngrok.io/
   ```

4. Check webhook logs in AgentMail console
   - Dashboard → Webhooks → "Logs" tab
   - Should show successful POSTs to your endpoint

### Problem: Email processed but no Telegram notification

**Check:**
1. Are you using the correct Telegram user ID?
   - Should be: `8627745904` (Jason's ID)

2. Check the logs:
   ```bash
   tail -50 /tmp/email-webhook.log | grep TELEGRAM
   ```

3. Test manual Telegram send:
   ```bash
   openclaw message send -t telegram:8627745904 -m "Test message"
   ```

### Problem: Server crashes or stops

**Restart it:**
```bash
bash /home/jason/.openclaw/workspace/stop-email-webhook.sh
bash /home/jason/.openclaw/workspace/start-email-webhook.sh
```

**For persistent running:** Consider setting up as a systemd service or cron job to auto-restart.

---

## Files & Locations

```
/home/jason/.openclaw/workspace/
├── email-webhook-server.js           # Main webhook listener
├── email-handler.js                  # Parses sender info
├── email-telegram-notifier.js        # Formats notifications
├── start-email-webhook.sh            # Start script
├── stop-email-webhook.sh             # Stop script
├── agentmail-webhook-handler.py      # Python alternative
└── .agentmail-api-key                # API key (protected)
```

**Log file:** `/tmp/email-webhook.log`

**PID file:** `/tmp/email-webhook.pid`

---

## System Architecture

```
Email arrives
    ↓
AgentMail receives it
    ↓
AgentMail sends POST to webhook URL
    ↓
email-webhook-server.js processes it
    ↓
email-handler.js parses sender
    ↓
email-telegram-notifier.js formats message
    ↓
Telegram notification sent to you instantly
```

**Token cost:** ~100 tokens per email (only when emails arrive, not constant polling)

---

## Next Steps

1. ✅ Verify webhook server is running
   ```bash
   ps aux | grep email-webhook-server
   ```

2. ⏳ Update AgentMail webhook URL in console

3. ⏳ Send test email to `arcadegamecave@agentmail.to`

4. ✅ Verify Telegram notification arrives

5. ✅ Check logs to confirm everything worked

---

## Questions?

Check the logs for detailed error messages:
```bash
tail -50 /tmp/email-webhook.log
```

All email processing is logged with timestamps and status updates.
