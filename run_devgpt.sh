#!/bin/bash

# Check mode
MODE=${1:-local}  # default to "local", can be set to "docker"

echo "🚀 Running DevGPT ($MODE mode)"

# Local dev mode
if [ "$MODE" = "local" ]; then
  # Start backend
  echo "▶️ Starting FastAPI backend..."
  cd devgpt/backend || exit 1
  if [ ! -d "env" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv env
  fi
  source env/bin/activate
  pip install -r requirements.txt
  uvicorn main:app --reload --port 8000 &
  BACK_PID=$!
  cd ../..

  # Start frontend
  echo "▶️ Starting React frontend..."
  cd devgpt/frontend || exit 1
  npm install
  npm run dev &
  FRONT_PID=$!

  # Wait for user input to exit
  echo "🟢 DevGPT running: Frontend on http://localhost:3000, Backend on http://localhost:8000"
  echo "Press Ctrl+C to stop..."

  trap 'echo "⛔ Shutting down..."; kill $BACK_PID $FRONT_PID; exit 0' SIGINT
  wait

# Docker mode
elif [ "$MODE" = "docker" ]; then
  echo "🐳 Starting with Docker Compose..."
  cd devgpt || exit 1
  docker-compose up --build

else
  echo "❌ Invalid mode. Use: ./run-devgpt.sh [local|docker]"
  exit 1
fi
