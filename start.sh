#!/bin/bash

# TalentScout AI - Startup Script
# This script starts both backend and frontend

echo "🚀 Starting TalentScout AI..."
echo ""

# Check if .env exists in backend
if [ ! -f "backend/.env" ]; then
    echo "⚠️  Backend .env file not found!"
    echo "📝 Creating from template..."
    cp backend/env.example backend/.env
    echo "✅ Created backend/.env"
    echo "⚠️  Please edit backend/.env and add your OPENAI_API_KEY"
    echo ""
fi

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
    echo "✅ Frontend dependencies installed"
    echo ""
fi

# Start both services
echo "🎯 Starting backend and frontend..."
echo "   Backend: http://localhost:8000"
echo "   Frontend: http://localhost:5173"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both services"
echo ""

npm run dev

