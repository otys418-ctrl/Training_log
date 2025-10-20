#!/bin/bash

# Stop All Services

echo "🛑 Stopping Progressive Overload Log Services..."

if [ -f /tmp/polog_pids.txt ]; then
    PIDS=$(cat /tmp/polog_pids.txt)
    kill $PIDS 2>/dev/null
    echo "✅ Services stopped"
    rm /tmp/polog_pids.txt
else
    echo "No PIDs file found. Killing by port..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    lsof -ti:8001 | xargs kill -9 2>/dev/null
    lsof -ti:5173 | xargs kill -9 2>/dev/null
    echo "✅ Ports cleared"
fi
