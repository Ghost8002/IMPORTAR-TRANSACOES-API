#!/usr/bin/env python3
"""
Script de teste para verificar se a API está funcionando
"""

import requests
import json
import time
import os
from datetime import datetime

class APITester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def test_health_check(self):
        """Testa o endpoint de health check"""
        print("🔍 Testando health check...")
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check OK - Status: {data['status']}")
                return True
            else:
                print(f"❌ Health check falhou - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Erro no health check: {str(e)}")
            return False
    
    def test_process_ofx(self):
        """Testa o processamento de arquivo OFX"""
        print("📁 Testando processamento OFX...")
        
        # Verificar se existe arquivo de teste
        test_file = "TRANSAÇÕES.ofx"
        if not os.path.exists(test_file):
            print(f"⚠️ Arquivo de teste '{test_file}' não encontrado")
            return False
        
        try:
            with open(test_file, 'rb') as f:
                files = {'file': (test_file, f, 'application/ofx')}
                response = self.session.post(f"{self.base_url}/api/process-ofx", files=files)
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    transactions = data['data']['transactions']
                    stats = data['data']['statistics']
                    print(f"✅ Processamento OFX OK - {len(transactions)} transações processadas")
                    print(f"   📊 Estatísticas: {stats['total_transactions']} total, R$ {stats['saldo']:.2f} saldo")
                    return True
                else:
                    print(f"❌ Processamento OFX falhou: {data['error']}")
                    return False
            else:
                print(f"❌ Processamento OFX falhou - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Erro no processamento OFX: {str(e)}")
            return False
    
    def test_get_transactions(self):
        """Testa a busca de transações"""
        print("📋 Testando busca de transações...")
        try:
            response = self.session.get(f"{self.base_url}/api/transactions")
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    transactions = data['data']['transactions']
                    print(f"✅ Busca de transações OK - {len(transactions)} transações encontradas")
                    return True
                else:
                    print(f"❌ Busca de transações falhou: {data['error']}")
                    return False
            else:
                print(f"❌ Busca de transações falhou - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Erro na busca de transações: {str(e)}")
            return False
    
    def test_get_dashboard(self):
        """Testa o endpoint do dashboard"""
        print("📊 Testando dashboard...")
        try:
            response = self.session.get(f"{self.base_url}/api/dashboard")
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    dashboard_data = data['data']
                    print(f"✅ Dashboard OK - Saldo: R$ {dashboard_data['current_balance']:.2f}")
                    return True
                else:
                    print(f"❌ Dashboard falhou: {data['error']}")
                    return False
            else:
                print(f"❌ Dashboard falhou - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Erro no dashboard: {str(e)}")
            return False
    
    def test_get_categories(self):
        """Testa a busca de categorias"""
        print("📂 Testando busca de categorias...")
        try:
            response = self.session.get(f"{self.base_url}/api/categories")
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    categories = data['data']
                    print(f"✅ Busca de categorias OK - {len(categories)} categorias encontradas")
                    return True
                else:
                    print(f"❌ Busca de categorias falhou: {data['error']}")
                    return False
            else:
                print(f"❌ Busca de categorias falhou - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Erro na busca de categorias: {str(e)}")
            return False
    
    def test_add_transaction(self):
        """Testa a adição de transação"""
        print("➕ Testando adição de transação...")
        try:
            transaction = {
                "data": datetime.now().strftime('%Y-%m-%d'),
                "descricao": "Teste API",
                "valor": 100.00,
                "categoria": "Teste",
                "tipo": "Receita"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/transactions",
                json=transaction,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    print(f"✅ Adição de transação OK")
                    return True
                else:
                    print(f"❌ Adição de transação falhou: {data['error']}")
                    return False
            else:
                print(f"❌ Adição de transação falhou - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Erro na adição de transação: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Executa todos os testes"""
        print("🚀 Iniciando testes da API...")
        print("=" * 50)
        
        tests = [
            ("Health Check", self.test_health_check),
            ("Processamento OFX", self.test_process_ofx),
            ("Busca de Transações", self.test_get_transactions),
            ("Dashboard", self.test_get_dashboard),
            ("Busca de Categorias", self.test_get_categories),
            ("Adição de Transação", self.test_add_transaction)
        ]
        
        results = []
        for test_name, test_func in tests:
            print(f"\n🧪 {test_name}")
            print("-" * 30)
            try:
                result = test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"❌ Erro inesperado: {str(e)}")
                results.append((test_name, False))
        
        # Resumo dos resultados
        print("\n" + "=" * 50)
        print("📊 RESUMO DOS TESTES")
        print("=" * 50)
        
        passed = 0
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASSOU" if result else "❌ FALHOU"
            print(f"{test_name}: {status}")
            if result:
                passed += 1
        
        print(f"\n🎯 Resultado: {passed}/{total} testes passaram")
        
        if passed == total:
            print("🎉 Todos os testes passaram! A API está funcionando corretamente.")
        else:
            print("⚠️ Alguns testes falharam. Verifique a configuração da API.")
        
        return passed == total

def main():
    """Função principal"""
    print("🧪 Testador da API de Processamento OFX")
    print("=" * 50)
    
    # Verificar se a API está rodando
    tester = APITester()
    
    try:
        # Tentar conectar com a API
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code != 200:
            print("❌ API não está respondendo. Certifique-se de que ela está rodando:")
            print("   python start_api.py")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar com a API. Certifique-se de que ela está rodando:")
        print("   python start_api.py")
        return False
    
    # Executar testes
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 API pronta para uso!")
        print("📚 Consulte a documentação em API_DOCUMENTATION.md")
    else:
        print("\n⚠️ Alguns problemas foram encontrados.")
        print("🔧 Verifique os logs da API e tente novamente.")
    
    return success

if __name__ == '__main__':
    main() 