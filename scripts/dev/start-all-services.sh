#!/bin/bash

# Script de démarrage rapide pour tester Auth0 migration
# Mode: Bypass (sans Auth0 configuré)

set -e

echo "🚀 Starting Trading Bot Services (Bypass Mode)"
echo "================================================"

# Configuration
export AUTH0_BYPASS=1
export ENTITLEMENTS_BYPASS=1
export DATABASE_URL="postgresql://user:password@localhost:5432/trading_bot"

# Couleurs pour les logs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

# Fonction pour démarrer un service backend
start_backend() {
    local name=$1
    local port=$2
    local path=$3

    echo -e "${BLUE}Starting $name on port $port...${NC}"
    cd "$ROOT_DIR/$path"
    python -m uvicorn app.main:app --host 0.0.0.0 --port "$port" --reload > "/tmp/${name}.log" 2>&1 &
    echo $! > "/tmp/${name}.pid"
    cd - > /dev/null
    sleep 2

    # Vérifier que le service démarre
    if curl -s "http://localhost:$port/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ $name started successfully${NC}"
    else
        echo -e "⚠️  $name may not be ready yet (check /tmp/${name}.log)"
    fi
}

# Fonction pour démarrer un service frontend
start_frontend() {
    local name=$1
    local port=$2
    local path=$3

    echo -e "${BLUE}Starting $name on port $port...${NC}"
    cd "$ROOT_DIR/$path"
    npm run dev -- --port "$port" > "/tmp/${name}.log" 2>&1 &
    echo $! > "/tmp/${name}.pid"
    cd - > /dev/null
    sleep 3
    echo -e "${GREEN}✅ $name started (check /tmp/${name}.log)${NC}"
}

echo ""
echo "📦 Starting Backend Services..."
echo "================================"

# 1. auth_gateway_service
start_backend "auth_gateway" "8012" "services/auth_gateway_service"

# 2. algo_engine
start_backend "algo_engine" "8000" "services/algo_engine"

# 3. user_service
start_backend "user_service" "8001" "services/user_service"

echo ""
echo "🌐 Starting Frontend Services..."
echo "================================="

# 4. auth_portal
start_frontend "auth_portal" "3000" "services/auth_portal"

# 5. web_dashboard
start_frontend "web_dashboard" "8022" "services/web_dashboard"

echo ""
echo "================================================"
echo -e "${GREEN}✅ All services started!${NC}"
echo ""
echo "📍 Service URLs:"
echo "   - Auth Gateway:   http://localhost:8012"
echo "   - Algo Engine:    http://localhost:8000"
echo "   - User Service:   http://localhost:8001"
echo "   - Auth Portal:    http://localhost:3000"
echo "   - Web Dashboard:  http://localhost:8022"
echo ""
echo "📋 Logs:"
echo "   - Backend logs:   /tmp/*.log"
echo "   - PIDs:           /tmp/*.pid"
echo ""
echo "⚠️  Note: Services are running in BYPASS MODE"
echo "   Auth0 authentication is disabled for testing"
echo ""
echo "🛑 To stop all services:"
echo "   $ROOT_DIR/scripts/dev/stop-all-services.sh"
echo ""
