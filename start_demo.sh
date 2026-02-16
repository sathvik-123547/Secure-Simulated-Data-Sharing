#!/bin/bash
# Kills existing ports
kill $(lsof -t -i:8000) 2>/dev/null
kill $(lsof -t -i:8001) 2>/dev/null
kill $(lsof -t -i:8002) 2>/dev/null
kill $(lsof -t -i:3000) 2>/dev/null

echo "Starting SecureData Microservices..."
nohup python3 -m uvicorn src.edge.api:app --host 127.0.0.1 --port 8000 > edge.log 2>&1 &
echo "Edge Service: http://127.0.0.1:8000"

nohup python3 -m uvicorn src.cloud.api:app --host 127.0.0.1 --port 8001 > cloud.log 2>&1 &
echo "Cloud Service: http://127.0.0.1:8001"

nohup python3 -m uvicorn src.tpa.api:app --host 127.0.0.1 --port 8002 > tpa.log 2>&1 &
echo "TPA Service: http://127.0.0.1:8002"

echo "Starting Dashboard..."
# Run python http server for frontend using a custom script to set update port if needed, 
# but python3 -m http.server defaults to 8000 which is taken. Use 3000.
nohup python3 -m http.server 3000 --directory src/frontend > dashboard.log 2>&1 &
echo "Dashboard: http://127.0.0.1:3000"

echo "All services started."
echo "Waiting 5s for services to initialize..."
sleep 5
echo "Injecting Demo Data..."
python3 inject_data.py

echo "------------------------------------------------"
echo "✅ Demo is Live!"
echo "   Dashboard: http://127.0.0.1:3000"
echo "------------------------------------------------"
echo "Press Ctrl+C to stop."
wait
