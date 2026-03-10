#!/bin/bash
# Stop the email webhook server

PID_FILE="/tmp/email-webhook.pid"

if [ -f "$PID_FILE" ]; then
  PID=$(cat "$PID_FILE")
  if kill -0 "$PID" 2>/dev/null; then
    kill $PID
    rm "$PID_FILE"
    echo "✅ Email webhook server stopped (PID: $PID)"
  else
    echo "❌ Process not running (stale PID: $PID)"
    rm "$PID_FILE"
  fi
else
  echo "❌ No PID file found. Server may not be running."
fi
