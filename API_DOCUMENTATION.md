# 📚 Documentação da API de Processamento OFX

## 🎯 Visão Geral

Esta API permite processar arquivos OFX (extratos bancários) e gerenciar transações financeiras. Ela fornece endpoints para:

- Processamento de arquivos OFX
- Gerenciamento de transações
- Consulta de dados do dashboard
- Geração de relatórios
- Gerenciamento de categorias

## 🚀 Como Usar

### 1. Iniciar a API

```bash
# Instalar dependências
pip install -r requirements.txt

# Iniciar a API
python start_api.py
```

A API estará disponível em: `http://localhost:5000`

### 2. Verificar se a API está funcionando

```bash
curl http://localhost:5000/health
```

Resposta esperada:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00",
  "version": "1.0.0"
}
```

## 📋 Endpoints da API

### 🔍 Health Check

**GET** `/health`

Verifica se a API está funcionando.

**Resposta:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00",
  "version": "1.0.0"
}
```

### 📁 Processar Arquivo OFX

**POST** `/api/process-ofx`

Processa um arquivo OFX e retorna as transações categorizadas.

**Parâmetros:**
- `file` (multipart/form-data): Arquivo OFX

**Resposta de Sucesso:**
```json
{
  "success": true,
  "data": {
    "transactions": [
      {
        "data": "2024-01-15",
        "descricao": "SUPERMERCADO ABC",
        "valor": -150.50,
        "categoria": "Alimentação",
        "tipo": "Despesa",
        "origem": "OFX"
      }
    ],
    "statistics": {
      "total_transactions": 50,
      "total_receitas": 5000.00,
      "total_despesas": 3000.00,
      "saldo": 2000.00,
      "categorias": {
        "Alimentação": {
          "count": 15,
          "total": 800.00
        }
      }
    }
  },
  "message": "50 transações processadas com sucesso"
}
```

**Resposta de Erro:**
```json
{
  "success": false,
  "error": "Nenhum arquivo enviado"
}
```

### 📋 Gerenciar Transações

#### Buscar Transações

**GET** `/api/transactions`

Busca transações com filtros opcionais.

**Parâmetros de Query:**
- `data_inicio` (opcional): Data de início (YYYY-MM-DD)
- `data_fim` (opcional): Data de fim (YYYY-MM-DD)
- `categoria` (opcional): Filtro por categoria
- `tipo` (opcional): Filtro por tipo (Receita/Despesa)
- `limit` (opcional): Limite de registros (padrão: 100)
- `offset` (opcional): Offset para paginação (padrão: 0)

**Exemplo:**
```bash
curl "http://localhost:5000/api/transactions?data_inicio=2024-01-01&categoria=Alimentação&limit=10"
```

**Resposta:**
```json
{
  "success": true,
  "data": {
    "transactions": [
      {
        "data": "2024-01-15",
        "descricao": "SUPERMERCADO ABC",
        "valor": -150.50,
        "categoria": "Alimentação",
        "tipo": "Despesa",
        "origem": "OFX"
      }
    ],
    "pagination": {
      "total": 50,
      "limit": 10,
      "offset": 0,
      "has_more": true
    }
  }
}
```

#### Adicionar Transação

**POST** `/api/transactions`

Adiciona uma nova transação.

**Body:**
```json
{
  "data": "2024-01-15",
  "descricao": "Salário",
  "valor": 5000.00,
  "categoria": "Receita",
  "tipo": "Receita"
}
```

**Resposta:**
```json
{
  "success": true,
  "message": "Transação adicionada com sucesso"
}
```

#### Adicionar Múltiplas Transações

**POST** `/api/transactions/bulk`

Adiciona múltiplas transações de uma vez.

**Body:**
```json
{
  "transactions": [
    {
      "data": "2024-01-15",
      "descricao": "Transação 1",
      "valor": 100.00,
      "categoria": "Alimentação",
      "tipo": "Despesa"
    },
    {
      "data": "2024-01-16",
      "descricao": "Transação 2",
      "valor": 200.00,
      "categoria": "Transporte",
      "tipo": "Despesa"
    }
  ]
}
```

**Resposta:**
```json
{
  "success": true,
  "message": "2 transações adicionadas com sucesso"
}
```

### 📊 Dashboard

**GET** `/api/dashboard`

Retorna dados para o dashboard.

**Resposta:**
```json
{
  "success": true,
  "data": {
    "current_balance": 5000.00,
    "balance_change": 1000.00,
    "monthly_income": 8000.00,
    "monthly_expenses": 3000.00,
    "total_transactions": 150,
    "recent_transactions": [
      {
        "data": "2024-01-15",
        "descricao": "Transação recente",
        "valor": -50.00,
        "categoria": "Alimentação",
        "tipo": "Despesa"
      }
    ]
  }
}
```

### 📂 Categorias

#### Buscar Categorias

**GET** `/api/categories`

Retorna lista de categorias disponíveis.

**Resposta:**
```json
{
  "success": true,
  "data": [
    "Alimentação",
    "Transporte",
    "Serviços",
    "Saúde",
    "Educação",
    "Lazer",
    "Transferência",
    "Outros"
  ]
}
```

#### Adicionar Categoria

**POST** `/api/categories`

Adiciona uma nova categoria.

**Body:**
```json
{
  "name": "Investimentos"
}
```

**Resposta:**
```json
{
  "success": true,
  "message": "Categoria \"Investimentos\" adicionada com sucesso"
}
```

### 📈 Relatórios

**POST** `/api/reports`

Gera relatório financeiro.

**Body:**
```json
{
  "periodo": "Último Mês",
  "data_inicio": "2024-01-01",
  "data_fim": "2024-01-31"
}
```

**Resposta:**
```json
{
  "success": true,
  "data": {
    "total_receitas": 8000.00,
    "total_despesas": 3000.00,
    "saldo": 5000.00,
    "num_transacoes": 50,
    "top_categories": [
      {
        "Categoria": "Alimentação",
        "Valor": 800.00
      },
      {
        "Categoria": "Transporte",
        "Valor": 500.00
      }
    ]
  }
}
```

## 🔧 Integração com JavaScript

### Exemplo de Uso do Cliente JavaScript

```javascript
// Importar o cliente
import { OFXApiClient } from './api_client.js';

// Criar instância do cliente
const apiClient = new OFXApiClient('http://localhost:5000');

// Processar arquivo OFX
async function processarArquivoOFX(file) {
    try {
        const result = await apiClient.processOFXFile(file);
        console.log('Transações processadas:', result.transactions);
        console.log('Estatísticas:', result.statistics);
        
        // Adicionar transações ao sistema
        await apiClient.addTransactionsBulk(result.transactions);
        
        alert('Arquivo processado com sucesso!');
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao processar arquivo: ' + error.message);
    }
}

// Buscar transações
async function buscarTransacoes() {
    try {
        const data = await apiClient.getTransactions({
            data_inicio: '2024-01-01',
            categoria: 'Alimentação',
            limit: 10
        });
        
        console.log('Transações:', data.transactions);
    } catch (error) {
        console.error('Erro:', error);
    }
}

// Buscar dados do dashboard
async function carregarDashboard() {
    try {
        const data = await apiClient.getDashboardData();
        console.log('Dados do dashboard:', data);
    } catch (error) {
        console.error('Erro:', error);
    }
}
```

### Exemplo de Integração no HTML

```html
<!DOCTYPE html>
<html>
<head>
    <title>Integração OFX</title>
</head>
<body>
    <input type="file" id="ofxFile" accept=".ofx">
    <button onclick="importarOFX()">Importar OFX</button>
    
    <script src="api_client.js"></script>
    <script>
        async function importarOFX() {
            const fileInput = document.getElementById('ofxFile');
            const file = fileInput.files[0];
            
            if (!file) {
                alert('Selecione um arquivo OFX');
                return;
            }
            
            try {
                await importOFXFile(
                    file,
                    (result) => {
                        alert(`Sucesso: ${result.message}`);
                        console.log('Estatísticas:', result.statistics);
                    },
                    (error) => {
                        alert(`Erro: ${error}`);
                    }
                );
            } catch (error) {
                alert('Erro inesperado: ' + error.message);
            }
        }
    </script>
</body>
</html>
```

## 🛠️ Configuração

### Variáveis de Ambiente

```bash
# Host da API (padrão: 0.0.0.0)
API_HOST=0.0.0.0

# Porta da API (padrão: 5000)
API_PORT=5000

# Modo debug (padrão: True)
API_DEBUG=True
```

### Estrutura de Arquivos

```
projeto/
├── api_server.py          # Servidor Flask
├── start_api.py           # Script de inicialização
├── api_client.js          # Cliente JavaScript
├── ofx_parser.py          # Parser OFX
├── transaction_manager.py # Gerenciador de transações
├── requirements.txt       # Dependências Python
├── exemplo_integracao.html # Exemplo de integração
└── API_DOCUMENTATION.md   # Esta documentação
```

## 🔒 Segurança

### Recomendações

1. **Validação de Arquivos**: Sempre valide o tipo e tamanho dos arquivos OFX
2. **Rate Limiting**: Implemente rate limiting para evitar sobrecarga
3. **Autenticação**: Adicione autenticação se necessário
4. **HTTPS**: Use HTTPS em produção
5. **CORS**: Configure CORS adequadamente para seu domínio

### Exemplo de Configuração de Segurança

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# CORS específico
CORS(app, origins=['https://seusite.com'])
```

## 🚨 Tratamento de Erros

### Códigos de Status HTTP

- `200`: Sucesso
- `400`: Erro de validação (dados inválidos)
- `404`: Recurso não encontrado
- `500`: Erro interno do servidor

### Estrutura de Erro

```json
{
  "success": false,
  "error": "Descrição do erro"
}
```

## 📞 Suporte

Para dúvidas ou problemas:

1. Verifique se a API está rodando: `curl http://localhost:5000/health`
2. Verifique os logs da API
3. Teste com um arquivo OFX válido
4. Verifique a conectividade de rede

## 🔄 Atualizações

### Versão 1.0.0
- Processamento básico de arquivos OFX
- Gerenciamento de transações
- Dashboard e relatórios
- API REST completa
- Cliente JavaScript 