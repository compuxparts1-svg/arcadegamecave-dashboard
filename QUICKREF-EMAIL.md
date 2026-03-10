# Email System - Quick Reference

## Check System Status
```bash
ps aux | grep email-webhook-server
tail -f /tmp/email-webhook.log
```

## Start/Stop
```bash
bash start-email-webhook.sh    # Start
bash stop-email-webhook.sh     # Stop
```

## Test Webhook
```bash
curl -X POST http://localhost:3000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "message.received",
    "message": {
      "from_": "Sender <email@domain.com>",
      "subject": "Subject",
      "text": "Message body"
    }
  }'
```

## AgentMail Console
- **URL:** https://console.agentmail.to
- **Webhook Config:** Dashboard → Webhooks
- **Webhook Endpoint:** `https://unimposed-hyman-cognoscitively.ngrok-free.dev/webhook`

## Check Logs
```bash
tail -20 /tmp/email-webhook.log         # Last 20 lines
tail -f /tmp/email-webhook.log          # Real-time
grep TELEGRAM /tmp/email-webhook.log    # Telegram sends only
```

## Manual Telegram Test
```bash
openclaw message send -t telegram:8627745904 -m "Test message"
```

## Files
- **Server:** `email-webhook-server.js` (port 3000)
- **Parser:** `email-handler.js`
- **Log:** `/tmp/email-webhook.log`
- **PID:** `/tmp/email-webhook.pid`

## How It Works
1. Email → AgentMail (webhook fires)
2. Webhook → Your server on port 3000
3. Server parses sender & formats notification
4. Telegram notification sent instantly

## If Something Breaks
1. Check logs: `tail -50 /tmp/email-webhook.log`
2. Verify server running: `ps aux | grep email-webhook-server`
3. Restart: `bash stop-email-webhook.sh && bash start-email-webhook.sh`
4. Test: Use curl test above
