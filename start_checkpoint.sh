#!/bin/bash
# Auto-Checkpoint Startup Script
# Starts automatic backup every 15 minutes in background

cd "$(dirname "$0")"

echo "🔄 Starting Auto-Checkpoint System..."
echo "   - Interval: 15 minutes"
echo "   - Max checkpoints: 10"
echo ""

# Start in background with nohup
nohup .venv/bin/python src/auto_checkpoint.py start > .checkpoints/auto_checkpoint.log 2>&1 &

PID=$!
echo "✓ Auto-checkpoint running (PID: $PID)"
echo "  Log: .checkpoints/auto_checkpoint.log"
echo ""
echo "To stop: kill $PID"
echo $PID > .checkpoints/checkpoint.pid
