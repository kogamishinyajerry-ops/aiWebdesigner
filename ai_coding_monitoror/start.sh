#!/bin/bash

# AI Coding Monitoror - Start Script

echo "🚀 Starting AI Coding Monitoror..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create data directory
mkdir -p backend/data

# Install dependencies
echo "📦 Installing dependencies..."
cd backend
pip install -q -r requirements.txt

# Start backend
echo "🖥 Starting backend server..."
python3 -m main &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend
echo "🌐 Starting frontend server..."
cd ../frontend
python3 -m http.server 8001 &
FRONTEND_PID=$!

echo ""
echo "✅ AI Coding Monitoror is running!"
echo ""
echo "📊 Dashboard: http://localhost:8001"
echo "🔧 API: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ All services stopped"
    exit 0
}

# Trap signals
trap cleanup SIGINT SIGTERM

# Wait for services
wait
