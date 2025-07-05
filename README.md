# 💰 Gerenciador Financeiro

Um software completo para gerenciar suas transações financeiras, desenvolvido em Streamlit.

## 🚀 Funcionalidades

### 📊 Dashboard
- **Visão geral** das suas finanças
- **Métricas principais**: saldo, receitas, despesas
- **Gráficos interativos** de categorias e fluxo de caixa
- **Transações recentes** em tempo real

### 📁 Importação de Dados
- **Arquivos OFX** (extratos bancários)
- **Importação manual** de transações
- **Categorização automática** baseada em palavras-chave
- **Validação** de dados importados

### 📋 Gerenciamento de Transações
- **Filtros avançados** por data, categoria e tipo
- **Edição** de transações existentes
- **Exportação** para CSV
- **Busca** e organização

### 📈 Relatórios
- **Relatórios personalizados** por período
- **Análise de gastos** por categoria
- **Evolução temporal** das finanças
- **Top categorias** de despesas

### ⚙️ Configurações
- **Gerenciamento de categorias** personalizadas
- **Regras de categorização** automática
- **Backup e restauração** de dados
- **Configurações** do sistema

## 🛠️ Instalação

1. **Clone o repositório**:
```bash
git clone <url-do-repositorio>
cd gerenciador-financeiro
```

2. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

3. **Execute a aplicação**:
```bash
streamlit run app.py
```

4. **Acesse no navegador**:
```
http://localhost:8501
```

## 📁 Estrutura do Projeto

```
gerenciador-financeiro/
├── app.py                 # Aplicação principal Streamlit
├── ofx_parser.py          # Parser para arquivos OFX
├── transaction_manager.py # Gerenciador de transações
├── requirements.txt       # Dependências Python
├── README.md             # Documentação
└── TRANSAÇÕES.ofx        # Arquivo de exemplo
```

## 🔧 Como Usar

### 1. Primeiro Acesso
- Acesse a aplicação no navegador
- Vá para "📁 Importar Dados"
- Faça upload do seu arquivo OFX

### 2. Importação de Dados
- **Arquivo OFX**: Arraste e solte seu arquivo OFX
- **Manual**: Adicione transações individualmente
- **Categorização**: O sistema categoriza automaticamente

### 3. Análise dos Dados
- **Dashboard**: Veja resumo geral
- **Transações**: Gerencie e filtre transações
- **Relatórios**: Gere relatórios personalizados

### 4. Configurações
- **Categorias**: Adicione categorias personalizadas
- **Regras**: Configure categorização automática
- **Backup**: Faça backup dos seus dados

## 📊 Formatos Suportados

### Arquivo OFX
- Extratos bancários
- Cartões de crédito
- Contas correntes
- Investimentos

### Exportação
- **CSV**: Para outros sistemas
- **JSON**: Backup completo
- **Excel**: Relatórios

## 🎯 Categorias Padrão

- **Alimentação**: Supermercados, restaurantes, padarias
- **Transporte**: Combustível, Uber, transporte público
- **Serviços**: Netflix, Spotify, contas
- **Saúde**: Farmácias, consultas médicas
- **Educação**: Cursos, material escolar
- **Lazer**: Cinema, viagens, entretenimento
- **Transferência**: PIX, TED, DOC
- **Outros**: Categorias não identificadas

## 🔒 Segurança

- **Dados locais**: Todas as informações ficam no seu computador
- **Sem internet**: Funciona offline
- **Backup**: Sistema de backup integrado
- **Privacidade**: Nenhum dado é enviado para servidores externos

## 🚀 Próximas Funcionalidades

- [ ] **Importação CSV**: Suporte a arquivos CSV
- [ ] **Gráficos avançados**: Mais tipos de visualização
- [ ] **Metas financeiras**: Definição e acompanhamento
- [ ] **Alertas**: Notificações de gastos
- [ ] **Multi-contas**: Gerenciamento de múltiplas contas
- [ ] **Exportação Excel**: Relatórios em Excel
- [ ] **API**: Integração com outros sistemas

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 📞 Suporte

Se você encontrar algum problema ou tiver sugestões:

1. Abra uma issue no GitHub
2. Descreva o problema detalhadamente
3. Inclua screenshots se possível
4. Especifique sua versão do Python e Streamlit

---

**Desenvolvido com ❤️ usando Streamlit** 