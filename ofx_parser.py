import re
from datetime import datetime
from dateutil import parser as date_parser

class OFXParser:
    def __init__(self):
        self.transactions = []
    
    def parse_ofx_file(self, file_path):
        """Parse um arquivo OFX e extrai as transações"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Encontrar todas as transações
            transaction_pattern = r'<STMTTRN>(.*?)</STMTTRN>'
            transactions_raw = re.findall(transaction_pattern, content, re.DOTALL)
            
            transactions = []
            for trans_raw in transactions_raw:
                transaction = self._parse_transaction(trans_raw)
                if transaction:
                    transactions.append(transaction)
            
            return transactions
            
        except Exception as e:
            print(f"Erro ao processar arquivo OFX: {str(e)}")
            return []
    
    def _parse_transaction(self, trans_raw):
        """Parse uma transação individual"""
        try:
            # Extrair dados da transação
            trntype = self._extract_tag(trans_raw, 'TRNTYPE')
            dtposted = self._extract_tag(trans_raw, 'DTPOSTED')
            trnamt = self._extract_tag(trans_raw, 'TRNAMT')
            memo = self._extract_tag(trans_raw, 'MEMO')
            
            # Converter data
            date = self._parse_ofx_date(dtposted)
            
            # Converter valor
            amount = float(trnamt) if trnamt else 0.0
            
            # Determinar tipo
            tipo = "Receita" if amount > 0 else "Despesa"
            
            # Categorizar automaticamente
            categoria = self._categorize_transaction(memo)
            
            return {
                'data': date.strftime('%Y-%m-%d'),
                'descricao': memo or "Transação sem descrição",
                'valor': amount,
                'categoria': categoria,
                'tipo': tipo,
                'origem': 'OFX'
            }
            
        except Exception as e:
            print(f"Erro ao processar transação: {str(e)}")
            return None
    
    def _extract_tag(self, content, tag):
        """Extrai o valor de uma tag XML"""
        pattern = f'<{tag}>(.*?)</{tag}>'
        match = re.search(pattern, content, re.DOTALL)
        return match.group(1) if match else None
    
    def _parse_ofx_date(self, date_str):
        """Converte data OFX para datetime"""
        try:
            # Formato OFX: YYYYMMDDHHMMSS[timezone]
            if date_str:
                # Remover timezone se presente
                date_clean = re.sub(r'\[.*?\]', '', date_str)
                # Converter para datetime
                return datetime.strptime(date_clean, '%Y%m%d%H%M%S')
            return datetime.now()
        except:
            return datetime.now()
    
    def _categorize_transaction(self, description):
        """Categoriza automaticamente uma transação baseada na descrição"""
        if not description:
            return "Outros"
        
        desc_lower = description.lower()
        
        # Regras de categorização
        categories = {
            'Alimentação': [
                'supermercado', 'supermer', 'mercado', 'padaria', 'panificadora',
                'restaurante', 'lanchonete', 'pizzaria', 'hamburgueria', 'burger',
                'delicias', 'caseira', 'mix', 'cebola', 'mercado', 'gigantao'
            ],
            'Transporte': [
                'posto', 'combustível', 'gasolina', 'uber', '99', 'taxi',
                'metro', 'ônibus', 'estacionamento'
            ],
            'Serviços': [
                'netflix', 'spotify', 'youtube', 'amazon', 'google',
                'telefone', 'internet', 'energia', 'água', 'gás'
            ],
            'Saúde': [
                'farmácia', 'drogaria', 'médico', 'hospital', 'consulta',
                'exame', 'medicamento'
            ],
            'Educação': [
                'escola', 'universidade', 'curso', 'livro', 'material escolar'
            ],
            'Lazer': [
                'cinema', 'teatro', 'show', 'viagem', 'hotel', 'passeio'
            ],
            'Transferência': [
                'transferência', 'pix', 'ted', 'doc', 'pagamento'
            ]
        }
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in desc_lower:
                    return category
        
        return "Outros" 