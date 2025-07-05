#!/usr/bin/env python3
"""
Script para iniciar a API de Processamento OFX
"""

import os
import sys
from api_server import app

def main():
    """Função principal para iniciar a API"""
    
    # Configurações da API
    HOST = os.getenv('API_HOST', '0.0.0.0')
    PORT = int(os.getenv('API_PORT', 5000))
    DEBUG = os.getenv('API_DEBUG', 'True').lower() == 'true'
    
    print("🚀 Iniciando API de Processamento OFX...")
    print(f"📍 Host: {HOST}")
    print(f"🔌 Porta: {PORT}")
    print(f"🐛 Debug: {DEBUG}")
    print("=" * 50)
    
    try:
        # Iniciar servidor Flask
        app.run(
            host=HOST,
            port=PORT,
            debug=DEBUG,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n⏹️ API interrompida pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar API: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 