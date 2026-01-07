#!/bin/bash

# Script pour stopper tous les services

set -e

echo "🛑 Stopping Trading Bot Services..."
echo "===================================="

# Fonction pour stopper un service
stop_service() {
    local name=$1
    local pidfile="/tmp/${name}.pid"

    if [ -f "$pidfile" ]; then
        pid=$(cat "$pidfile")
        if ps -p "$pid" > /dev/null 2>&1; then
            echo "Stopping $name (PID: $pid)..."
            kill "$pid" 2>/dev/null || true
            rm "$pidfile"
            echo "✅ $name stopped"
        else
            echo "⚠️  $name (PID: $pid) not running"
            rm "$pidfile"
        fi
    else
        echo "ℹ️  No PID file for $name"
    fi
}

# Stopper les services
stop_service "auth_gateway"
stop_service "algo_engine"
stop_service "user_service"
stop_service "auth_portal"
stop_service "web_dashboard"

# Cleanup: Tuer tous les process restants
echo ""
echo "Cleaning up remaining processes..."
pkill -f "uvicorn.*app.main" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true

echo ""
echo "===================================="
echo "✅ All services stopped"
echo ""
echo "📋 Logs are still available in /tmp/*.log"
echo "   To view: tail -f /tmp/auth_gateway.log"
echo ""
