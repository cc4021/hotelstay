#!/bin/bash

# Hotel Booking System Deployment Script

echo "🏨 Hotel Booking System Deployment"
echo "=================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python installation
if command_exists python3; then
    PYTHON_CMD="python3"
elif command_exists python; then
    PYTHON_CMD="python"
else
    echo "❌ Python not found. Please install Python 3.11 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
echo "🐍 Found Python $PYTHON_VERSION"

# Install dependencies
echo "📦 Installing dependencies..."
$PYTHON_CMD -m pip install -r deployment_requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Set environment variable if not set
if [ -z "$SESSION_SECRET" ]; then
    export SESSION_SECRET="hotel-booking-secret-$(date +%s)"
    echo "🔑 Generated session secret"
fi

# Choose deployment mode
echo ""
echo "Choose deployment mode:"
echo "1) Development (python main.py)"
echo "2) Production (gunicorn)"
echo "3) Docker build"
echo "4) Test installation only"
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo "🚀 Starting development server..."
        $PYTHON_CMD main.py
        ;;
    2)
        echo "🚀 Starting production server with Gunicorn..."
        if command_exists gunicorn; then
            gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
        else
            echo "❌ Gunicorn not found. Installing..."
            $PYTHON_CMD -m pip install gunicorn
            gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
        fi
        ;;
    3)
        echo "🐳 Building Docker image..."
        if command_exists docker; then
            docker build -t hotel-booking-system .
            echo "✅ Docker image built successfully"
            echo "Run with: docker run -p 5000:5000 hotel-booking-system"
        else
            echo "❌ Docker not found. Please install Docker first."
        fi
        ;;
    4)
        echo "✅ Installation test completed successfully"
        echo "📋 Project files:"
        ls -la
        echo ""
        echo "🌐 To start the application:"
        echo "   Development: python main.py"
        echo "   Production:  gunicorn --bind 0.0.0.0:5000 main:app"
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac