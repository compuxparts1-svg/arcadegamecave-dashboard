#!/bin/bash
# LobsterBoard Dashboard Server
# Run this to start the LobsterBoard dashboard on port 8080

cd /home/jason/.openclaw/workspace

echo "🦞 Starting LobsterBoard Dashboard..."
echo "📊 Dashboard available at: http://localhost:8080"
echo "✏️  Press Ctrl+E to enter edit mode"
echo ""
echo "Custom widgets available:"
echo "  • Daily Profits (tracks all platforms)"
echo ""

PORT=8080 node node_modules/lobsterboard/server.cjs
