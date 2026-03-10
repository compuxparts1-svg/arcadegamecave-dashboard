#!/bin/bash
# Process queued email → Telegram messages
# Run this via cron every 5-10 seconds for automatic delivery

QUEUE_DIR="/tmp/email-telegram-queue"

if [ ! -d "$QUEUE_DIR" ]; then
  exit 0
fi

# Get all pending messages
for msg_file in "$QUEUE_DIR"/msg-*.json; do
  [ -f "$msg_file" ] || continue
  
  # Extract user ID and message
  USER_ID=$(jq -r '.userId' "$msg_file" 2>/dev/null)
  MESSAGE=$(jq -r '.message' "$msg_file" 2>/dev/null)
  
  if [ -z "$USER_ID" ] || [ -z "$MESSAGE" ]; then
    continue
  fi
  
  # Send via OpenClaw
  if openclaw message send -t "telegram:$USER_ID" -m "$MESSAGE" > /dev/null 2>&1; then
    # Success - remove from queue
    rm "$msg_file"
  fi
done
