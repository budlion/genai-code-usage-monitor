#!/bin/bash

# GenAI Code Usage Monitor Startup Script
# Usage: ./start_monitor.sh [options]

cd "$(dirname "$0")"

echo "🚀 Starting GenAI Code Usage Monitor..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Run monitor with provided options or defaults
PYTHONPATH=$(pwd)/src python -m genai_code_usage_monitor "$@"
