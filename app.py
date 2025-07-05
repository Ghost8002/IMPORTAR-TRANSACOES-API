import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from ofx_parser import OFXParser
from transaction_manager import TransactionManager

# Configuração da página
st.set_page_config(
    page_title="Gerenciador Financeiro",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .positive { color: #28a745; }
    .negative { color: #dc3545; }
    .stButton > button {
        width: 100%;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Inicialização do gerenciador de transações
@st.cache_resource
def get_transaction_manager():
    return TransactionManager()

transaction_manager = get_transaction_manager()

# Sidebar
with st.sidebar:
    st.markdown("## 📊 Menu")
    
    page = st.selectbox(
        "Escolha uma página:",
        ["🏠 Dashboard", "📁 Importar Dados", "📋 Transações", "📈 Relatórios", "⚙️ Configurações"]
    )

# Página Dashboard
if page == "🏠 Dashboard":
    st.markdown('<h1 class="main-header">💰 Gerenciador Financeiro</h1>', unsafe_allow_html=True)
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Saldo Atual",
            value=f"R$ {transaction_manager.get_current_balance():.2f}",
            delta=f"R$ {transaction_manager.get_balance_change():.2f}"
        )
    
    with col2:
        st.metric(
            label="Receitas (Mês)",
            value=f"R$ {transaction_manager.get_monthly_income():.2f}",
            delta="+"
        )
    
    with col3:
        st.metric(
            label="Despesas (Mês)",
            value=f"R$ {transaction_manager.get_monthly_expenses():.2f}",
            delta="-"
        )
    
    with col4:
        st.metric(
            label="Total Transações",
            value=transaction_manager.get_total_transactions()
        )
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Despesas por Categoria")
        category_chart = transaction_manager.get_category_chart()
        if category_chart is not None:
            st.plotly_chart(category_chart, use_container_width=True)
        else:
            st.info("Nenhuma transação encontrada. Importe dados para ver os gráficos.")
    
    with col2:
        st.subheader("📈 Fluxo de Caixa (Últimos 30 dias)")
        cashflow_chart = transaction_manager.get_cashflow_chart()
        if cashflow_chart is not None:
            st.plotly_chart(cashflow_chart, use_container_width=True)
        else:
            st.info("Nenhuma transação encontrada. Importe dados para ver os gráficos.")
    
    # Transações recentes
    st.subheader("🕒 Transações Recentes")
    recent_transactions = transaction_manager.get_recent_transactions(10)
    if not recent_transactions.empty:
        st.dataframe(
            recent_transactions[['data', 'descricao', 'valor', 'categoria', 'tipo']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Nenhuma transação encontrada. Importe dados para ver as transações.")

# Página Importar Dados
elif page == "📁 Importar Dados":
    st.markdown('<h1 class="main-header">📁 Importar Dados</h1>', unsafe_allow_html=True)
    
    # Upload de arquivo OFX
    st.subheader("📄 Importar Arquivo OFX")
    uploaded_file = st.file_uploader(
        "Escolha um arquivo OFX:",
        type=['ofx'],
        help="Arraste e solte seu arquivo OFX aqui"
    )
    
    if uploaded_file is not None:
        try:
            # Salvar arquivo temporariamente
            with open("temp_ofx.ofx", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Processar arquivo
            parser = OFXParser()
            transactions = parser.parse_ofx_file("temp_ofx.ofx")
            
            if transactions:
                st.success(f"✅ {len(transactions)} transações importadas com sucesso!")
                
                # Mostrar preview
                df_preview = pd.DataFrame(transactions)
                st.subheader("📋 Preview das Transações")
                st.dataframe(df_preview.head(10), use_container_width=True)
                
                # Botão para salvar
                if st.button("💾 Salvar Transações"):
                    transaction_manager.add_transactions(transactions)
                    st.success("Transações salvas com sucesso!")
                    
                    # Limpar arquivo temporário
                    os.remove("temp_ofx.ofx")
            else:
                st.error("❌ Nenhuma transação encontrada no arquivo.")
                
        except Exception as e:
            st.error(f"❌ Erro ao processar arquivo: {str(e)}")
    
    # Importação manual
    st.subheader("✏️ Adicionar Transação Manual")
    
    with st.form("manual_transaction"):
        col1, col2 = st.columns(2)
        
        with col1:
            data = st.date_input("Data da transação")
            descricao = st.text_input("Descrição")
            valor = st.number_input("Valor (R$)", min_value=0.01, step=0.01)
        
        with col2:
            tipo = st.selectbox("Tipo", ["Receita", "Despesa"])
            categoria = st.selectbox(
                "Categoria",
                transaction_manager.get_categories()
            )
        
        submitted = st.form_submit_button("➕ Adicionar Transação")
        
        if submitted:
            transaction = {
                'data': data.strftime('%Y-%m-%d'),
                'descricao': descricao,
                'valor': valor if tipo == "Receita" else -valor,
                'categoria': categoria,
                'tipo': tipo
            }
            
            transaction_manager.add_transaction(transaction)
            st.success("✅ Transação adicionada com sucesso!")

# Página Transações
elif page == "📋 Transações":
    st.markdown('<h1 class="main-header">📋 Gerenciar Transações</h1>', unsafe_allow_html=True)
    
    # Filtros
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        data_inicio = st.date_input("Data Início")
    
    with col2:
        data_fim = st.date_input("Data Fim")
    
    with col3:
        categoria_filtro = st.selectbox("Categoria", ["Todas"] + transaction_manager.get_categories())
    
    with col4:
        tipo_filtro = st.selectbox("Tipo", ["Todos", "Receita", "Despesa"])
    
    # Aplicar filtros
    filtered_transactions = transaction_manager.get_filtered_transactions(
        data_inicio, data_fim, categoria_filtro, tipo_filtro
    )
    
    if not filtered_transactions.empty:
        st.subheader(f"📊 {len(filtered_transactions)} Transações Encontradas")
        
        # Estatísticas dos filtros
        total_receitas = filtered_transactions[filtered_transactions['valor'] > 0]['valor'].sum()
        total_despesas = abs(filtered_transactions[filtered_transactions['valor'] < 0]['valor'].sum())
        saldo = total_receitas - total_despesas
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Receitas", f"R$ {total_receitas:.2f}")
        with col2:
            st.metric("Despesas", f"R$ {total_despesas:.2f}")
        with col3:
            st.metric("Saldo", f"R$ {saldo:.2f}")
        
        # Tabela de transações
        st.dataframe(
            filtered_transactions,
            use_container_width=True,
            hide_index=True
        )
        
        # Botões de ação
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Exportar CSV"):
                csv = filtered_transactions.to_csv(index=False)
                st.download_button(
                    label="💾 Download CSV",
                    data=csv,
                    file_name=f"transacoes_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("🗑️ Limpar Todas"):
                if st.checkbox("Confirmar exclusão de todas as transações"):
                    transaction_manager.clear_all_transactions()
                    st.success("Todas as transações foram removidas!")
                    st.rerun()
    else:
        st.info("Nenhuma transação encontrada com os filtros aplicados.")

# Página Relatórios
elif page == "📈 Relatórios":
    st.markdown('<h1 class="main-header">📈 Relatórios</h1>', unsafe_allow_html=True)
    
    # Seleção de período
    col1, col2 = st.columns(2)
    
    with col1:
        periodo = st.selectbox(
            "Período do Relatório",
            ["Último Mês", "Últimos 3 Meses", "Último Ano", "Personalizado"]
        )
    
    with col2:
        if periodo == "Personalizado":
            data_inicio = st.date_input("Data Início")
            data_fim = st.date_input("Data Fim")
        else:
            data_inicio = None
            data_fim = None
    
    # Gerar relatório
    if st.button("📊 Gerar Relatório"):
        report_data = transaction_manager.generate_report(periodo, data_inicio, data_fim)
        
        if report_data:
            # Resumo executivo
            st.subheader("📋 Resumo Executivo")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Receitas", f"R$ {report_data['total_receitas']:.2f}")
            with col2:
                st.metric("Total Despesas", f"R$ {report_data['total_despesas']:.2f}")
            with col3:
                st.metric("Saldo", f"R$ {report_data['saldo']:.2f}")
            with col4:
                st.metric("Nº Transações", report_data['num_transacoes'])
            
            # Gráficos do relatório
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Distribuição por Categoria")
                if report_data['category_chart']:
                    st.plotly_chart(report_data['category_chart'], use_container_width=True)
            
            with col2:
                st.subheader("📈 Evolução Mensal")
                if report_data['monthly_chart']:
                    st.plotly_chart(report_data['monthly_chart'], use_container_width=True)
            
            # Top categorias
            st.subheader("🏆 Top 5 Categorias")
            if not report_data['top_categories'].empty:
                st.dataframe(report_data['top_categories'], use_container_width=True)
            else:
                st.info("Nenhuma categoria encontrada para o período selecionado.")
        else:
            st.warning("Nenhum dado encontrado para o período selecionado.")

# Página Configurações
elif page == "⚙️ Configurações":
    st.markdown('<h1 class="main-header">⚙️ Configurações</h1>', unsafe_allow_html=True)
    
    # Gerenciar categorias
    st.subheader("📂 Gerenciar Categorias")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Categorias Existentes:**")
        categories = transaction_manager.get_categories()
        for cat in categories:
            st.write(f"• {cat}")
    
    with col2:
        with st.form("add_category"):
            nova_categoria = st.text_input("Nova Categoria")
            submitted = st.form_submit_button("➕ Adicionar Categoria")
            
            if submitted and nova_categoria:
                transaction_manager.add_category(nova_categoria)
                st.success(f"Categoria '{nova_categoria}' adicionada!")
                st.rerun()
    
    # Regras de categorização
    st.subheader("🎯 Regras de Categorização Automática")
    
    rules = transaction_manager.get_categorization_rules()
    
    if rules:
        st.write("**Regras Ativas:**")
        for keyword, category in rules.items():
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"'{keyword}' → {category}")
            with col2:
                if st.button(f"✏️ Editar", key=f"edit_{keyword}"):
                    # Implementar edição
                    pass
            with col3:
                if st.button(f"🗑️ Remover", key=f"remove_{keyword}"):
                    transaction_manager.remove_categorization_rule(keyword)
                    st.success("Regra removida!")
                    st.rerun()
    
    # Adicionar nova regra
    with st.form("add_rule"):
        col1, col2 = st.columns(2)
        
        with col1:
            keyword = st.text_input("Palavra-chave")
        
        with col2:
            category = st.selectbox("Categoria", transaction_manager.get_categories())
        
        submitted = st.form_submit_button("➕ Adicionar Regra")
        
        if submitted and keyword and category:
            transaction_manager.add_categorization_rule(keyword, category)
            st.success(f"Regra adicionada: '{keyword}' → {category}")
            st.rerun()
    
    # Backup e Restauração
    st.subheader("💾 Backup e Restauração")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Fazer Backup"):
            backup_data = transaction_manager.export_data()
            st.download_button(
                label="💾 Download Backup",
                data=json.dumps(backup_data, indent=2),
                file_name=f"backup_financeiro_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        uploaded_backup = st.file_uploader(
            "Restaurar Backup:",
            type=['json'],
            help="Selecione um arquivo de backup"
        )
        
        if uploaded_backup:
            if st.button("🔄 Restaurar Dados"):
                try:
                    backup_data = json.load(uploaded_backup)
                    transaction_manager.import_data(backup_data)
                    st.success("Backup restaurado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao restaurar backup: {str(e)}")

# Rodapé
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>💰 Gerenciador Financeiro - Desenvolvido com Streamlit</div>",
    unsafe_allow_html=True
) 