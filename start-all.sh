#!/bin/bash

# Start All Services for Progressive Overload Log
# This script starts P-MIS, L-DPS, and S-RE in the background

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "🚀 Starting Progressive Overload Log Services..."
echo ""

# Start P-MIS (port 8000)
echo "1️⃣ Starting P-MIS on port 8000..."
cd "$SCRIPT_DIR/pmis"
python3 main.py > /tmp/pmis.log 2>&1 &
PMIS_PID=$!
echo "   P-MIS started (PID: $PMIS_PID)"

# Start L-DPS (port 8001)
echo "2️⃣ Starting L-DPS on port 8001..."
cd "$SCRIPT_DIR/ldps"
python3 main.py > /tmp/ldps.log 2>&1 &
LDPS_PID=$!
echo "   L-DPS started (PID: $LDPS_PID)"

# Start S-RE (port 5173)
echo "3️⃣ Starting S-RE on port 5173..."
cd "$SCRIPT_DIR/sre"
npm run dev > /tmp/sre.log 2>&1 &
SRE_PID=$!
echo "   S-RE started (PID: $SRE_PID)"

echo ""
echo "✅ All services starting..."
echo ""
echo "Wait 5 seconds for services to initialize..."
sleep 5

echo ""
echo "📊 Service Status:"
echo "   P-MIS:  http://localhost:8000 (PID: $PMIS_PID)"
echo "   L-DPS:  http://localhost:8001 (PID: $LDPS_PID)"
echo "   S-RE:   http://localhost:5173 (PID: $SRE_PID)"
echo ""
echo "🌐 Open your browser: http://localhost:5173"
echo ""
echo "📝 Logs:"
echo "   P-MIS: tail -f /tmp/pmis.log"
echo "   L-DPS: tail -f /tmp/ldps.log"
echo "   S-RE:  tail -f /tmp/sre.log"
echo ""
echo "🛑 To stop all services, run:"
echo "   kill $PMIS_PID $LDPS_PID $SRE_PID"
echo ""

# Save PIDs to file for easy stopping later
echo "$PMIS_PID $LDPS_PID $SRE_PID" > /tmp/polog_pids.txt
