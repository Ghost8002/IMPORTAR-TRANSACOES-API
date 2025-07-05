import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os

class TransactionManager:
    def __init__(self):
        self.data_file = "transactions.json"
        self.categories_file = "categories.json"
        self.rules_file = "categorization_rules.json"
        self.transactions = self._load_transactions()
        self.categories = self._load_categories()
        self.categorization_rules = self._load_categorization_rules()
    
    def _load_transactions(self):
        """Carrega transações do arquivo JSON"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return pd.DataFrame(data)
            return pd.DataFrame(columns=['data', 'descricao', 'valor', 'categoria', 'tipo', 'origem'])
        except:
            return pd.DataFrame(columns=['data', 'descricao', 'valor', 'categoria', 'tipo', 'origem'])
    
    def _save_transactions(self):
        """Salva transações no arquivo JSON"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.transactions.to_dict('records'), f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar transações: {str(e)}")
    
    def _load_categories(self):
        """Carrega categorias do arquivo JSON"""
        try:
            if os.path.exists(self.categories_file):
                with open(self.categories_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return [
                "Alimentação", "Transporte", "Serviços", "Saúde", "Educação",
                "Lazer", "Transferência", "Outros"
            ]
        except:
            return [
                "Alimentação", "Transporte", "Serviços", "Saúde", "Educação",
                "Lazer", "Transferência", "Outros"
            ]
    
    def _save_categories(self):
        """Salva categorias no arquivo JSON"""
        try:
            with open(self.categories_file, 'w', encoding='utf-8') as f:
                json.dump(self.categories, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar categorias: {str(e)}")
    
    def _load_categorization_rules(self):
        """Carrega regras de categorização do arquivo JSON"""
        try:
            if os.path.exists(self.rules_file):
                with open(self.rules_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except:
            return {}
    
    def _save_categorization_rules(self):
        """Salva regras de categorização no arquivo JSON"""
        try:
            with open(self.rules_file, 'w', encoding='utf-8') as f:
                json.dump(self.categorization_rules, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar regras: {str(e)}")
    
    def add_transaction(self, transaction):
        """Adiciona uma transação"""
        # Aplicar regras de categorização se não houver categoria
        if 'categoria' not in transaction or not transaction['categoria']:
            transaction['categoria'] = self._apply_categorization_rules(transaction['descricao'])
        
        # Adicionar origem se não especificada
        if 'origem' not in transaction:
            transaction['origem'] = 'Manual'
        
        # Converter para DataFrame e adicionar
        new_transaction = pd.DataFrame([transaction])
        if self.transactions.empty:
            self.transactions = new_transaction
        else:
            self.transactions = pd.concat([self.transactions, new_transaction], ignore_index=True)
        self._save_transactions()
    
    def add_transactions(self, transactions):
        """Adiciona múltiplas transações"""
        for transaction in transactions:
            self.add_transaction(transaction)
    
    def get_current_balance(self):
        """Calcula o saldo atual"""
        if self.transactions.empty:
            return 0.0
        return self.transactions['valor'].sum()
    
    def get_balance_change(self):
        """Calcula a mudança no saldo do mês atual"""
        if self.transactions.empty:
            return 0.0
        
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        # Filtrar transações do mês atual
        month_transactions = self.transactions[
            pd.to_datetime(self.transactions['data']).dt.month == current_month
        ]
        
        return month_transactions['valor'].sum()
    
    def get_monthly_income(self):
        """Calcula receitas do mês atual"""
        if self.transactions.empty:
            return 0.0
        
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        # Filtrar receitas do mês atual
        month_income = self.transactions[
            (pd.to_datetime(self.transactions['data']).dt.month == current_month) &
            (self.transactions['valor'] > 0)
        ]
        
        return month_income['valor'].sum()
    
    def get_monthly_expenses(self):
        """Calcula despesas do mês atual"""
        if self.transactions.empty:
            return 0.0
        
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        # Filtrar despesas do mês atual
        month_expenses = self.transactions[
            (pd.to_datetime(self.transactions['data']).dt.month == current_month) &
            (self.transactions['valor'] < 0)
        ]
        
        return abs(month_expenses['valor'].sum())
    
    def get_total_transactions(self):
        """Retorna o número total de transações"""
        return len(self.transactions)
    
    def get_recent_transactions(self, limit=10):
        """Retorna as transações mais recentes"""
        if self.transactions.empty:
            return pd.DataFrame()
        
        # Ordenar por data e retornar as mais recentes
        sorted_transactions = self.transactions.sort_values('data', ascending=False)
        return sorted_transactions.head(limit)
    
    def get_filtered_transactions(self, data_inicio=None, data_fim=None, categoria=None, tipo=None):
        """Retorna transações filtradas"""
        if self.transactions.empty:
            return pd.DataFrame()
        
        filtered = self.transactions.copy()
        
        # Filtrar por data
        if data_inicio:
            filtered = filtered[pd.to_datetime(filtered['data']) >= pd.to_datetime(data_inicio)]
        
        if data_fim:
            filtered = filtered[pd.to_datetime(filtered['data']) <= pd.to_datetime(data_fim)]
        
        # Filtrar por categoria
        if categoria and categoria != "Todas":
            filtered = filtered[filtered['categoria'] == categoria]
        
        # Filtrar por tipo
        if tipo and tipo != "Todos":
            if tipo == "Receita":
                filtered = filtered[filtered['valor'] > 0]
            elif tipo == "Despesa":
                filtered = filtered[filtered['valor'] < 0]
        
        return filtered.sort_values('data', ascending=False)
    
    def get_category_chart(self):
        """Gera gráfico de despesas por categoria"""
        if self.transactions.empty:
            return None
        
        # Filtrar apenas despesas
        expenses = self.transactions[self.transactions['valor'] < 0].copy()
        
        if expenses.empty:
            return None
        
        # Agrupar por categoria
        category_data = expenses.groupby('categoria')['valor'].sum().abs()
        
        if category_data.empty:
            return None
        
        # Criar gráfico
        fig = px.pie(
            values=category_data.values,
            names=category_data.index,
            title="Despesas por Categoria"
        )
        
        return fig
    
    def get_cashflow_chart(self):
        """Gera gráfico de fluxo de caixa"""
        if self.transactions.empty:
            return None
        
        # Filtrar últimos 30 dias
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_transactions = self.transactions[
            pd.to_datetime(self.transactions['data']) >= thirty_days_ago
        ].copy()
        
        if recent_transactions.empty:
            return None
        
        # Agrupar por data
        daily_data = recent_transactions.groupby('data')['valor'].sum().reset_index()
        daily_data['data'] = pd.to_datetime(daily_data['data'])
        daily_data = daily_data.sort_values('data')
        # Converter para datetime Python para evitar warning
        daily_data['data_python'] = daily_data['data'].dt.to_pydatetime()
        
        # Calcular saldo acumulado
        daily_data['saldo_acumulado'] = daily_data['valor'].cumsum()
        
        # Criar gráfico
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=daily_data['data_python'],
            y=daily_data['saldo_acumulado'],
            mode='lines+markers',
            name='Saldo Acumulado',
            line=dict(color='blue', width=2)
        ))
        
        fig.update_layout(
            title="Fluxo de Caixa - Últimos 30 Dias",
            xaxis_title="Data",
            yaxis_title="Saldo (R$)",
            hovermode='x unified'
        )
        
        return fig
    
    def get_categories(self):
        """Retorna lista de categorias"""
        return self.categories
    
    def add_category(self, category):
        """Adiciona uma nova categoria"""
        if category not in self.categories:
            self.categories.append(category)
            self._save_categories()
    
    def get_categorization_rules(self):
        """Retorna regras de categorização"""
        return self.categorization_rules
    
    def add_categorization_rule(self, keyword, category):
        """Adiciona uma regra de categorização"""
        self.categorization_rules[keyword.lower()] = category
        self._save_categorization_rules()
    
    def remove_categorization_rule(self, keyword):
        """Remove uma regra de categorização"""
        if keyword.lower() in self.categorization_rules:
            del self.categorization_rules[keyword.lower()]
            self._save_categorization_rules()
    
    def _apply_categorization_rules(self, description):
        """Aplica regras de categorização a uma descrição"""
        if not description:
            return "Outros"
        
        desc_lower = description.lower()
        
        for keyword, category in self.categorization_rules.items():
            if keyword in desc_lower:
                return category
        
        return "Outros"
    
    def generate_report(self, periodo, data_inicio=None, data_fim=None):
        """Gera relatório financeiro"""
        if self.transactions.empty:
            return None
        
        # Determinar período
        if periodo == "Último Mês":
            data_inicio = (datetime.now() - timedelta(days=30)).date()
            data_fim = datetime.now().date()
        elif periodo == "Últimos 3 Meses":
            data_inicio = (datetime.now() - timedelta(days=90)).date()
            data_fim = datetime.now().date()
        elif periodo == "Último Ano":
            data_inicio = (datetime.now() - timedelta(days=365)).date()
            data_fim = datetime.now().date()
        
        # Filtrar transações do período
        if data_inicio and data_fim:
            filtered_transactions = self.get_filtered_transactions(data_inicio, data_fim)
        else:
            filtered_transactions = self.transactions.copy()
        
        if filtered_transactions.empty:
            return None
        
        # Calcular métricas
        total_receitas = filtered_transactions[filtered_transactions['valor'] > 0]['valor'].sum()
        total_despesas = abs(filtered_transactions[filtered_transactions['valor'] < 0]['valor'].sum())
        saldo = total_receitas - total_despesas
        num_transacoes = len(filtered_transactions)
        
        # Top categorias
        expenses = filtered_transactions[filtered_transactions['valor'] < 0]
        if not expenses.empty:
            top_categories = expenses.groupby('categoria')['valor'].sum().abs().sort_values(ascending=False).head(5)
            top_categories_df = pd.DataFrame({
                'Categoria': top_categories.index,
                'Valor': top_categories.values
            })
        else:
            top_categories_df = pd.DataFrame()
        
        # Gráficos
        category_chart = None
        if not expenses.empty:
            category_data = expenses.groupby('categoria')['valor'].sum().abs()
            category_chart = px.pie(
                values=category_data.values,
                names=category_data.index,
                title="Distribuição por Categoria"
            )
        
        monthly_chart = None
        if not filtered_transactions.empty:
            monthly_data = filtered_transactions.copy()
            monthly_data['data'] = pd.to_datetime(monthly_data['data'])
            monthly_data['mes'] = monthly_data['data'].dt.to_period('M')
            monthly_summary = monthly_data.groupby('mes')['valor'].sum().reset_index()
            monthly_summary['mes'] = monthly_summary['mes'].astype(str)
            
            monthly_chart = px.bar(
                monthly_summary,
                x='mes',
                y='valor',
                title="Evolução Mensal",
                color='valor',
                color_continuous_scale=['red', 'green']
            )
        
        return {
            'total_receitas': total_receitas,
            'total_despesas': total_despesas,
            'saldo': saldo,
            'num_transacoes': num_transacoes,
            'top_categories': top_categories_df,
            'category_chart': category_chart,
            'monthly_chart': monthly_chart
        }
    
    def clear_all_transactions(self):
        """Remove todas as transações"""
        self.transactions = pd.DataFrame(columns=['data', 'descricao', 'valor', 'categoria', 'tipo', 'origem'])
        self._save_transactions()
    
    def export_data(self):
        """Exporta todos os dados"""
        return {
            'transactions': self.transactions.to_dict('records'),
            'categories': self.categories,
            'categorization_rules': self.categorization_rules
        }
    
    def import_data(self, data):
        """Importa dados de backup"""
        if 'transactions' in data:
            self.transactions = pd.DataFrame(data['transactions'])
            self._save_transactions()
        
        if 'categories' in data:
            self.categories = data['categories']
            self._save_categories()
        
        if 'categorization_rules' in data:
            self.categorization_rules = data['categorization_rules']
            self._save_categorization_rules() 