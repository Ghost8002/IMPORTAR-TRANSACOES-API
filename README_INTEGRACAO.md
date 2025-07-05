# 🔗 Guia de Integração - API de Processamento OFX

## 🎯 O que foi criado

Transformei seu sistema de processamento OFX em uma **API REST** que pode ser consumida pelo seu sistema de gerenciamento financeiro. Agora você pode:

1. **Importar arquivos OFX** através de uma API
2. **Receber transações já categorizadas** automaticamente
3. **Integrar facilmente** com qualquer sistema web/mobile
4. **Manter a funcionalidade** de categorização automática

## 🚀 Como usar

### 1. **Iniciar a API**

```bash
# Instalar dependências
pip install -r requirements.txt

# Iniciar a API
python start_api.py
```

A API estará disponível em: `http://localhost:5000`

### 2. **Testar se está funcionando**

```bash
# Executar testes automatizados
python test_api.py
```

### 3. **Integrar no seu sistema financeiro**

#### **Opção A: Usando JavaScript (Recomendado)**

```javascript
// Incluir o cliente da API
<script src="api_client.js"></script>

// Função para importar OFX
async function importarOFX() {
    const fileInput = document.getElementById('ofxFile');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Selecione um arquivo OFX');
        return;
    }
    
    try {
        // Processar arquivo OFX
        const apiClient = new OFXApiClient('http://localhost:5000');
        const result = await apiClient.processOFXFile(file);
        
        // Adicionar transações ao sistema
        await apiClient.addTransactionsBulk(result.transactions);
        
        alert(`Sucesso! ${result.transactions.length} transações importadas`);
        
        // Atualizar lista de transações no seu sistema
        carregarTransacoes();
        
    } catch (error) {
        alert('Erro: ' + error.message);
    }
}

// Função para carregar transações
async function carregarTransacoes() {
    try {
        const apiClient = new OFXApiClient('http://localhost:5000');
        const data = await apiClient.getTransactions();
        
        // Atualizar sua tabela de transações
        atualizarTabelaTransacoes(data.transactions);
        
    } catch (error) {
        console.error('Erro ao carregar transações:', error);
    }
}
```

#### **Opção B: Usando HTML simples**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Importar OFX</title>
</head>
<body>
    <h2>Importar Extrato OFX</h2>
    
    <input type="file" id="ofxFile" accept=".ofx">
    <button onclick="importarOFX()">Importar</button>
    
    <div id="resultado"></div>
    
    <script src="api_client.js"></script>
    <script>
        async function importarOFX() {
            const fileInput = document.getElementById('ofxFile');
            const file = fileInput.files[0];
            
            if (!file) {
                alert('Selecione um arquivo OFX');
                return;
            }
            
            const resultado = document.getElementById('resultado');
            resultado.innerHTML = 'Processando...';
            
            try {
                await importOFXFile(
                    file,
                    (result) => {
                        resultado.innerHTML = `
                            <h3>✅ Sucesso!</h3>
                            <p>${result.message}</p>
                            <p>Total de transações: ${result.transactions.length}</p>
                            <p>Saldo: R$ ${result.statistics.saldo.toFixed(2)}</p>
                        `;
                    },
                    (error) => {
                        resultado.innerHTML = `<h3>❌ Erro: ${error}</h3>`;
                    }
                );
            } catch (error) {
                resultado.innerHTML = `<h3>❌ Erro inesperado: ${error.message}</h3>`;
            }
        }
    </script>
</body>
</html>
```

#### **Opção C: Usando fetch diretamente**

```javascript
async function importarOFXFetch(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        // Processar arquivo
        const response = await fetch('http://localhost:5000/api/process-ofx', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Adicionar transações
            const addResponse = await fetch('http://localhost:5000/api/transactions/bulk', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    transactions: result.data.transactions
                })
            });
            
            const addResult = await addResponse.json();
            
            if (addResult.success) {
                alert(`Sucesso! ${result.data.transactions.length} transações importadas`);
            }
        } else {
            alert('Erro: ' + result.error);
        }
    } catch (error) {
        alert('Erro de conexão: ' + error.message);
    }
}
```

## 📋 Endpoints principais

### **Processar OFX**
```
POST /api/process-ofx
```
- **Entrada**: Arquivo OFX
- **Saída**: Transações categorizadas + estatísticas

### **Buscar Transações**
```
GET /api/transactions
```
- **Parâmetros**: data_inicio, data_fim, categoria, tipo, limit, offset
- **Saída**: Lista de transações com paginação

### **Adicionar Transações**
```
POST /api/transactions/bulk
```
- **Entrada**: Array de transações
- **Saída**: Confirmação de sucesso

### **Dashboard**
```
GET /api/dashboard
```
- **Saída**: Métricas financeiras em tempo real

## 🔧 Integração no seu sistema

### **1. Adicionar botão de importação**

No seu sistema financeiro, adicione um botão como este:

```html
<div class="import-section">
    <h3>Importar Extrato OFX</h3>
    <input type="file" id="ofxFile" accept=".ofx" style="display: none;">
    <button class="btn btn-primary" onclick="document.getElementById('ofxFile').click()">
        📁 Selecionar Arquivo OFX
    </button>
    <button class="btn btn-success" onclick="importarOFX()" id="importBtn" disabled>
        ⬆️ Importar Transações
    </button>
</div>
```

### **2. Implementar a lógica de importação**

```javascript
// Configurar listener para seleção de arquivo
document.getElementById('ofxFile').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        document.getElementById('importBtn').disabled = false;
        document.getElementById('importBtn').textContent = `⬆️ Importar ${file.name}`;
    }
});

// Função de importação
async function importarOFX() {
    const fileInput = document.getElementById('ofxFile');
    const file = fileInput.files[0];
    
    if (!file) return;
    
    // Mostrar loading
    const btn = document.getElementById('importBtn');
    btn.disabled = true;
    btn.textContent = '⏳ Processando...';
    
    try {
        const apiClient = new OFXApiClient();
        
        // Processar arquivo
        const result = await apiClient.processOFXFile(file);
        
        // Adicionar transações
        await apiClient.addTransactionsBulk(result.transactions);
        
        // Sucesso
        alert(`✅ ${result.transactions.length} transações importadas com sucesso!`);
        
        // Limpar arquivo
        fileInput.value = '';
        btn.disabled = true;
        btn.textContent = '⬆️ Importar Transações';
        
        // Atualizar lista de transações
        if (typeof carregarTransacoes === 'function') {
            carregarTransacoes();
        }
        
    } catch (error) {
        alert('❌ Erro: ' + error.message);
        btn.disabled = false;
        btn.textContent = '⬆️ Importar Transações';
    }
}
```

### **3. Atualizar lista de transações**

```javascript
async function carregarTransacoes() {
    try {
        const apiClient = new OFXApiClient();
        const data = await apiClient.getTransactions({
            limit: 100,
            offset: 0
        });
        
        // Atualizar sua tabela/lista de transações
        const tbody = document.getElementById('transactionsTable');
        tbody.innerHTML = '';
        
        data.transactions.forEach(transaction => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${formatDate(transaction.data)}</td>
                <td>${transaction.descricao}</td>
                <td class="${transaction.valor > 0 ? 'positive' : 'negative'}">
                    R$ ${Math.abs(transaction.valor).toFixed(2)}
                </td>
                <td><span class="badge">${transaction.categoria}</span></td>
                <td>${transaction.tipo}</td>
            `;
            tbody.appendChild(row);
        });
        
    } catch (error) {
        console.error('Erro ao carregar transações:', error);
    }
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('pt-BR');
}
```

## 🎨 Exemplo completo de integração

Veja o arquivo `exemplo_integracao.html` para um exemplo completo e funcional de como integrar a API no seu sistema.

## 🔒 Configuração de segurança

### **Para produção, configure:**

```python
# No arquivo api_server.py
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# CORS específico para seu domínio
CORS(app, origins=['https://seusite.com'])

# Rate limiting
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)
```

## 🚨 Solução de problemas

### **API não responde**
```bash
# Verificar se está rodando
curl http://localhost:5000/health

# Reiniciar se necessário
python start_api.py
```

### **Erro de CORS**
- Verifique se o CORS está configurado corretamente
- Adicione seu domínio na lista de origens permitidas

### **Arquivo não processado**
- Verifique se é um arquivo OFX válido
- Verifique o tamanho do arquivo (máximo 16MB)
- Verifique os logs da API

## 📞 Suporte

Se encontrar problemas:

1. **Execute os testes**: `python test_api.py`
2. **Verifique os logs** da API
3. **Teste com um arquivo OFX válido**
4. **Verifique a conectividade** de rede

## 🎉 Próximos passos

Com a API funcionando, você pode:

1. **Integrar no seu sistema** usando os exemplos acima
2. **Personalizar categorias** através da API
3. **Adicionar autenticação** se necessário
4. **Implementar cache** para melhor performance
5. **Adicionar mais endpoints** conforme necessário

A API está pronta para uso! 🚀 