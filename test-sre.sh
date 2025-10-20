#!/bin/bash

# S-RE Test Script
# Tests all three services and their integration

echo "🧪 Testing S-RE Application..."
echo ""

# Test P-MIS
echo "1️⃣ Testing P-MIS (port 8000)..."
if curl -s http://localhost:8000 > /dev/null; then
    echo "✅ P-MIS is running"
else
    echo "❌ P-MIS is not running. Start it with: cd pmis && python3 main.py"
    exit 1
fi

# Test L-DPS
echo "2️⃣ Testing L-DPS (port 8001)..."
if curl -s http://localhost:8001 > /dev/null; then
    echo "✅ L-DPS is running"
else
    echo "❌ L-DPS is not running. Start it with: cd ldps && python3 main.py"
    exit 1
fi

# Test S-RE
echo "3️⃣ Testing S-RE (port 5173)..."
if curl -s http://localhost:5173 > /dev/null; then
    echo "✅ S-RE is running"
else
    echo "❌ S-RE is not running. Start it with: cd sre && npm run dev"
    exit 1
fi

echo ""
echo "✅ All services running!"
echo ""
echo "📱 Open your browser: http://localhost:5173"
echo ""
echo "🧪 Manual Test Steps:"
echo "  1. View workout list"
echo "  2. Click 'Start Exercise' on any exercise"
echo "  3. Log a set (weight + reps)"
echo "  4. Verify set appears in current session"
echo "  5. Click 'Finish Exercise'"
echo "  6. Return to same exercise to see progressive overload"
