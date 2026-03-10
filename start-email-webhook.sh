#!/bin/bash
# Start the email webhook server as a background process

WEBHOOK_DIR="/home/jason/.openclaw/workspace"
LOG_FILE="/tmp/email-webhook.log"
PID_FILE="/tmp/email-webhook.pid"

# Check if already running
if [ -f "$PID_FILE" ]; then
  OLD_PID=$(cat "$PID_FILE")
  if kill -0 "$OLD_PID" 2>/dev/null; then
    echo "❌ Email webhook server is already running (PID: $OLD_PID)"
    exit 1
  fi
fi

# Start the server
cd "$WEBHOOK_DIR"
nohup node email-webhook-server.js > "$LOG_FILE" 2>&1 &
NEW_PID=$!
echo $NEW_PID > "$PID_FILE"

echo "✅ Email webhook server started (PID: $NEW_PID)"
echo "   Log file: $LOG_FILE"
echo "   To stop: kill $NEW_PID"
echo "   Or run: bash stop-email-webhook.sh"
