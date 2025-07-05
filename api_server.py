from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
from werkzeug.utils import secure_filename
from ofx_parser import OFXParser
from transaction_manager import TransactionManager
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Permite requisições de outros domínios

# Configurações
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'ofx'}

# Inicializar o gerenciador de transações
transaction_manager = TransactionManager()

def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de verificação de saúde da API"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/process-ofx', methods=['POST'])
def process_ofx():
    """
    Processa arquivo OFX e retorna transações categorizadas
    
    Returns:
        JSON com transações processadas e estatísticas
    """
    try:
        # Verificar se arquivo foi enviado
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Nenhum arquivo enviado'
            }), 400
        
        file = request.files['file']
        
        # Verificar se arquivo foi selecionado
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Nenhum arquivo selecionado'
            }), 400
        
        # Verificar extensão
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Tipo de arquivo não permitido. Use apenas arquivos .ofx'
            }), 400
        
        # Salvar arquivo temporariamente
        with tempfile.NamedTemporaryFile(delete=False, suffix='.ofx') as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name
        
        try:
            # Processar arquivo OFX
            parser = OFXParser()
            transactions = parser.parse_ofx_file(temp_file_path)
            
            if not transactions:
                return jsonify({
                    'success': False,
                    'error': 'Nenhuma transação encontrada no arquivo OFX'
                }), 400
            
            # Calcular estatísticas
            total_transactions = len(transactions)
            total_receitas = sum(t['valor'] for t in transactions if t['valor'] > 0)
            total_despesas = abs(sum(t['valor'] for t in transactions if t['valor'] < 0))
            
            # Agrupar por categoria
            categorias = {}
            for t in transactions:
                cat = t['categoria']
                if cat not in categorias:
                    categorias[cat] = {'count': 0, 'total': 0}
                categorias[cat]['count'] += 1
                categorias[cat]['total'] += abs(t['valor'])
            
            return jsonify({
                'success': True,
                'data': {
                    'transactions': transactions,
                    'statistics': {
                        'total_transactions': total_transactions,
                        'total_receitas': total_receitas,
                        'total_despesas': total_despesas,
                        'saldo': total_receitas - total_despesas,
                        'categorias': categorias
                    }
                },
                'message': f'{total_transactions} transações processadas com sucesso'
            })
            
        finally:
            # Limpar arquivo temporário
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao processar arquivo: {str(e)}'
        }), 500

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """
    Retorna transações com filtros opcionais
    
    Query Parameters:
        - data_inicio: Data de início (YYYY-MM-DD)
        - data_fim: Data de fim (YYYY-MM-DD)
        - categoria: Filtro por categoria
        - tipo: Filtro por tipo (Receita/Despesa)
        - limit: Limite de registros (padrão: 100)
        - offset: Offset para paginação (padrão: 0)
    """
    try:
        # Parâmetros de filtro
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        categoria = request.args.get('categoria')
        tipo = request.args.get('tipo')
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))
        
        # Converter datas se fornecidas
        if data_inicio:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        if data_fim:
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        
        # Buscar transações filtradas
        filtered_transactions = transaction_manager.get_filtered_transactions(
            data_inicio, data_fim, categoria, tipo
        )
        
        # Aplicar paginação
        total_count = len(filtered_transactions)
        paginated_transactions = filtered_transactions.iloc[offset:offset+limit]
        
        return jsonify({
            'success': True,
            'data': {
                'transactions': paginated_transactions.to_dict('records'),
                'pagination': {
                    'total': total_count,
                    'limit': limit,
                    'offset': offset,
                    'has_more': offset + limit < total_count
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao buscar transações: {str(e)}'
        }), 500

@app.route('/api/transactions', methods=['POST'])
def add_transaction():
    """
    Adiciona uma nova transação
    
    Body:
        JSON com dados da transação
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Dados da transação não fornecidos'
            }), 400
        
        # Validar campos obrigatórios
        required_fields = ['data', 'descricao', 'valor']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Campo obrigatório não fornecido: {field}'
                }), 400
        
        # Adicionar transação
        transaction_manager.add_transaction(data)
        
        return jsonify({
            'success': True,
            'message': 'Transação adicionada com sucesso'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao adicionar transação: {str(e)}'
        }), 500

@app.route('/api/transactions/bulk', methods=['POST'])
def add_transactions_bulk():
    """
    Adiciona múltiplas transações de uma vez
    
    Body:
        JSON com array de transações
    """
    try:
        data = request.get_json()
        
        if not data or 'transactions' not in data:
            return jsonify({
                'success': False,
                'error': 'Array de transações não fornecido'
            }), 400
        
        transactions = data['transactions']
        
        if not isinstance(transactions, list):
            return jsonify({
                'success': False,
                'error': 'transactions deve ser um array'
            }), 400
        
        # Adicionar transações
        transaction_manager.add_transactions(transactions)
        
        return jsonify({
            'success': True,
            'message': f'{len(transactions)} transações adicionadas com sucesso'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao adicionar transações: {str(e)}'
        }), 500

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard_data():
    """
    Retorna dados para o dashboard
    """
    try:
        return jsonify({
            'success': True,
            'data': {
                'current_balance': transaction_manager.get_current_balance(),
                'balance_change': transaction_manager.get_balance_change(),
                'monthly_income': transaction_manager.get_monthly_income(),
                'monthly_expenses': transaction_manager.get_monthly_expenses(),
                'total_transactions': transaction_manager.get_total_transactions(),
                'recent_transactions': transaction_manager.get_recent_transactions(10).to_dict('records')
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao buscar dados do dashboard: {str(e)}'
        }), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """
    Retorna lista de categorias disponíveis
    """
    try:
        return jsonify({
            'success': True,
            'data': transaction_manager.get_categories()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao buscar categorias: {str(e)}'
        }), 500

@app.route('/api/categories', methods=['POST'])
def add_category():
    """
    Adiciona uma nova categoria
    """
    try:
        data = request.get_json()
        
        if not data or 'name' not in data:
            return jsonify({
                'success': False,
                'error': 'Nome da categoria não fornecido'
            }), 400
        
        transaction_manager.add_category(data['name'])
        
        return jsonify({
            'success': True,
            'message': f'Categoria "{data["name"]}" adicionada com sucesso'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao adicionar categoria: {str(e)}'
        }), 500

@app.route('/api/reports', methods=['POST'])
def generate_report():
    """
    Gera relatório financeiro
    
    Body:
        JSON com parâmetros do relatório
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Parâmetros do relatório não fornecidos'
            }), 400
        
        periodo = data.get('periodo', 'Último Mês')
        data_inicio = data.get('data_inicio')
        data_fim = data.get('data_fim')
        
        # Converter datas se fornecidas
        if data_inicio:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        if data_fim:
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        
        report_data = transaction_manager.generate_report(periodo, data_inicio, data_fim)
        
        if not report_data:
            return jsonify({
                'success': False,
                'error': 'Nenhum dado encontrado para o período selecionado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'total_receitas': report_data['total_receitas'],
                'total_despesas': report_data['total_despesas'],
                'saldo': report_data['saldo'],
                'num_transacoes': report_data['num_transacoes'],
                'top_categories': report_data['top_categories'].to_dict('records') if not report_data['top_categories'].empty else []
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao gerar relatório: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 