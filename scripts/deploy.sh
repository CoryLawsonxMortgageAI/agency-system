#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════════
# Agency Management System - Deployment Script
# ═══════════════════════════════════════════════════════════════════════════════

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="agency-system"
DEPLOY_ENV="${1:-development}"
PLATFORM="${2:-local}"

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║              🏢 AGENCY MANAGEMENT SYSTEM DEPLOYER               ║"
echo "║                   Autonomous Agent Platform                      ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${BLUE}▶ Environment: $DEPLOY_ENV${NC}"
echo -e "${BLUE}▶ Platform: $PLATFORM${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# Helper Functions
# ═══════════════════════════════════════════════════════════════════════════════

log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1"
}

# ═══════════════════════════════════════════════════════════════════════════════
# Pre-deployment Checks
# ═══════════════════════════════════════════════════════════════════════════════

check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is not installed"
        exit 1
    fi
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        log_error "Node.js is not installed"
        exit 1
    fi
    
    # Check environment file
    if [ ! -f ".env" ]; then
        log_warning ".env file not found, creating from example..."
        cp .env.example .env
        log_warning "Please edit .env and add your API keys before continuing"
        exit 1
    fi
    
    log_success "Prerequisites check passed"
}

# ═══════════════════════════════════════════════════════════════════════════════
# Python Backend Setup
# ═══════════════════════════════════════════════════════════════════════════════

setup_backend() {
    log_info "Setting up Python backend..."
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        log_info "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install dependencies
    log_info "Installing Python dependencies..."
    pip install -r requirements.txt
    
    log_success "Backend setup complete"
}

# ═══════════════════════════════════════════════════════════════════════════════
# Frontend Setup
# ═══════════════════════════════════════════════════════════════════════════════

setup_frontend() {
    log_info "Setting up frontend..."
    
    cd ui
    
    # Install dependencies
    if [ ! -d "node_modules" ]; then
        log_info "Installing Node.js dependencies..."
        npm install
    fi
    
    cd ..
    
    log_success "Frontend setup complete"
}

# ═══════════════════════════════════════════════════════════════════════════════
# Local Deployment
# ═══════════════════════════════════════════════════════════════════════════════

deploy_local() {
    log_info "Starting local deployment..."
    
    # Setup backend and frontend
    setup_backend
    setup_frontend
    
    log_success "Local deployment ready!"
    echo ""
    echo -e "${GREEN}To start the system:${NC}"
    echo "  1. Terminal 1: source venv/bin/activate && cd api && python main.py"
    echo "  2. Terminal 2: cd ui && npm run dev"
    echo "  3. Terminal 3: python agency-cli.py status"
    echo ""
    echo -e "${GREEN}Access points:${NC}"
    echo "  - API: http://localhost:8000"
    echo "  - UI: http://localhost:3000"
    echo "  - Docs: http://localhost:8000/docs"
}

# ═══════════════════════════════════════════════════════════════════════════════
# Docker Deployment
# ═══════════════════════════════════════════════════════════════════════════════

deploy_docker() {
    log_info "Building Docker containers..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed"
        exit 1
    fi
    
    # Build and start
    docker-compose up --build -d
    
    log_success "Docker deployment complete!"
    echo ""
    echo -e "${GREEN}Access points:${NC}"
    echo "  - API: http://localhost:8000"
    echo "  - UI: http://localhost:3000"
}

# ═══════════════════════════════════════════════════════════════════════════════
# Vercel Deployment
# ═══════════════════════════════════════════════════════════════════════════════

deploy_vercel() {
    log_info "Deploying to Vercel..."
    
    # Check Vercel CLI
    if ! command -v vercel &> /dev/null; then
        log_info "Installing Vercel CLI..."
        npm install -g vercel
    fi
    
    # Deploy frontend
    cd ui
    vercel --prod
    cd ..
    
    log_success "Vercel deployment initiated!"
    log_warning "Note: Backend needs separate deployment (Railway/Render/AWS)"
}

# ═══════════════════════════════════════════════════════════════════════════════
# Railway Deployment
# ═══════════════════════════════════════════════════════════════════════════════

deploy_railway() {
    log_info "Deploying to Railway..."
    
    # Check Railway CLI
    if ! command -v railway &> /dev/null; then
        log_info "Installing Railway CLI..."
        npm install -g @railway/cli
    fi
    
    # Login if needed
    railway login
    
    # Initialize and deploy
    railway init
    railway up
    
    log_success "Railway deployment complete!"
}

# ═══════════════════════════════════════════════════════════════════════════════
# Render Deployment
# ═══════════════════════════════════════════════════════════════════════════════

deploy_render() {
    log_info "Generating Render configuration..."
    
    cat > render.yaml << EOF
services:
  - type: web
    name: agency-api
    runtime: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "cd api && uvicorn main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: OPENAI_API_KEY
        sync: false
      - key: ANTHROPIC_API_KEY
        sync: false

  - type: web
    name: agency-ui
    runtime: static
    buildCommand: "cd ui && npm install && npm run build"
    staticPublishPath: ./ui/dist
    envVars:
      - key: NODE_VERSION
        value: 18
EOF
    
    log_success "Render configuration generated: render.yaml"
    log_info "Push to GitHub and connect to Render for automatic deployment"
}

# ═══════════════════════════════════════════════════════════════════════════════
# Health Check
# ═══════════════════════════════════════════════════════════════════════════════

health_check() {
    log_info "Running health check..."
    
    # Check API
    if curl -s http://localhost:8000/health > /dev/null; then
        log_success "API is healthy"
    else
        log_error "API health check failed"
    fi
    
    # Check UI
    if curl -s http://localhost:3000 > /dev/null; then
        log_success "UI is accessible"
    else
        log_warning "UI not yet accessible (may still be building)"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# Main Execution
# ═══════════════════════════════════════════════════════════════════════════════

main() {
    check_prerequisites
    
    case $PLATFORM in
        local)
            deploy_local
            ;;
        docker)
            deploy_docker
            ;;
        vercel)
            deploy_vercel
            ;;
        railway)
            deploy_railway
            ;;
        render)
            deploy_render
            ;;
        *)
            log_error "Unknown platform: $PLATFORM"
            echo "Supported platforms: local, docker, vercel, railway, render"
            exit 1
            ;;
    esac
    
    echo ""
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  🏢 Agency Management System deployment complete!${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo ""
}

# Run main function
main
