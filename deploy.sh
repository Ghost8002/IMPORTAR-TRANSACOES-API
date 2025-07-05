#!/bin/bash

# Script de deploy para diferentes plataformas
# Uso: ./deploy.sh [plataforma]

set -e

PLATFORM=${1:-render}

echo "🚀 Iniciando deploy para $PLATFORM..."

case $PLATFORM in
    "render")
        echo "📦 Deployando para Render..."
        # Render detecta automaticamente o build
        echo "✅ Push para GitHub ativará deploy automático"
        ;;
        
    "railway")
        echo "📦 Deployando para Railway..."
        if command -v railway &> /dev/null; then
            railway up
        else
            echo "❌ Railway CLI não encontrado. Instale com: npm i -g @railway/cli"
        fi
        ;;
        
    "heroku")
        echo "📦 Deployando para Heroku..."
        if command -v heroku &> /dev/null; then
            git push heroku main
        else
            echo "❌ Heroku CLI não encontrado. Instale com: npm install -g heroku"
        fi
        ;;
        
    "docker")
        echo "📦 Deployando com Docker..."
        docker build -t ofx-api .
        docker run -p 5000:8080 ofx-api
        ;;
        
    "docker-compose")
        echo "📦 Deployando com Docker Compose..."
        docker-compose up --build -d
        ;;
        
    "local")
        echo "📦 Executando localmente..."
        python start_api.py
        ;;
        
    *)
        echo "❌ Plataforma não reconhecida: $PLATFORM"
        echo "Plataformas disponíveis: render, railway, heroku, docker, docker-compose, local"
        exit 1
        ;;
esac

echo "✅ Deploy concluído!" 