/**
 * Cliente JavaScript para API de Processamento OFX
 * 
 * Este arquivo contém funções para consumir a API de processamento
 * de arquivos OFX e gerenciamento de transações.
 */

class OFXApiClient {
    constructor(baseUrl = 'https://importar-transacoes-api.onrender.com') {
        this.baseUrl = baseUrl;
    }

    /**
     * Verifica se a API está funcionando
     */
    async healthCheck() {
        try {
            const response = await fetch(`${this.baseUrl}/health`);
            return await response.json();
        } catch (error) {
            console.error('Erro ao verificar saúde da API:', error);
            throw error;
        }
    }

    /**
     * Processa arquivo OFX e retorna transações categorizadas
     * @param {File} file - Arquivo OFX
     * @returns {Promise<Object>} Transações processadas
     */
    async processOFXFile(file) {
        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch(`${this.baseUrl}/api/process-ofx`, {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (!result.success) {
                throw new Error(result.error);
            }

            return result.data;
        } catch (error) {
            console.error('Erro ao processar arquivo OFX:', error);
            throw error;
        }
    }

    /**
     * Busca transações com filtros opcionais
     * @param {Object} filters - Filtros de busca
     * @returns {Promise<Object>} Transações filtradas
     */
    async getTransactions(filters = {}) {
        try {
            const params = new URLSearchParams();
            
            if (filters.data_inicio) params.append('data_inicio', filters.data_inicio);
            if (filters.data_fim) params.append('data_fim', filters.data_fim);
            if (filters.categoria) params.append('categoria', filters.categoria);
            if (filters.tipo) params.append('tipo', filters.tipo);
            if (filters.limit) params.append('limit', filters.limit);
            if (filters.offset) params.append('offset', filters.offset);

            const response = await fetch(`${this.baseUrl}/api/transactions?${params}`);
            const result = await response.json();

            if (!result.success) {
                throw new Error(result.error);
            }

            return result.data;
        } catch (error) {
            console.error('Erro ao buscar transações:', error);
            throw error;
        }
    }

    /**
     * Adiciona uma nova transação
     * @param {Object} transaction - Dados da transação
     * @returns {Promise<Object>} Resultado da operação
     */
    async addTransaction(transaction) {
        try {
            const response = await fetch(`${this.baseUrl}/api/transactions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(transaction)
            });

            const result = await response.json();

            if (!result.success) {
                throw new Error(result.error);
            }

            return result;
        } catch (error) {
            console.error('Erro ao adicionar transação:', error);
            throw error;
        }
    }

    /**
     * Adiciona múltiplas transações de uma vez
     * @param {Array} transactions - Array de transações
     * @returns {Promise<Object>} Resultado da operação
     */
    async addTransactionsBulk(transactions) {
        try {
            const response = await fetch(`${this.baseUrl}/api/transactions/bulk`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ transactions })
            });

            const result = await response.json();

            if (!result.success) {
                throw new Error(result.error);
            }

            return result;
        } catch (error) {
            console.error('Erro ao adicionar transações:', error);
            throw error;
        }
    }

    /**
     * Busca dados do dashboard
     * @returns {Promise<Object>} Dados do dashboard
     */
    async getDashboardData() {
        try {
            const response = await fetch(`${this.baseUrl}/api/dashboard`);
            const result = await response.json();

            if (!result.success) {
                throw new Error(result.error);
            }

            return result.data;
        } catch (error) {
            console.error('Erro ao buscar dados do dashboard:', error);
            throw error;
        }
    }

    /**
     * Busca categorias disponíveis
     * @returns {Promise<Array>} Lista de categorias
     */
    async getCategories() {
        try {
            const response = await fetch(`${this.baseUrl}/api/categories`);
            const result = await response.json();

            if (!result.success) {
                throw new Error(result.error);
            }

            return result.data;
        } catch (error) {
            console.error('Erro ao buscar categorias:', error);
            throw error;
        }
    }

    /**
     * Adiciona uma nova categoria
     * @param {string} name - Nome da categoria
     * @returns {Promise<Object>} Resultado da operação
     */
    async addCategory(name) {
        try {
            const response = await fetch(`${this.baseUrl}/api/categories`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name })
            });

            const result = await response.json();

            if (!result.success) {
                throw new Error(result.error);
            }

            return result;
        } catch (error) {
            console.error('Erro ao adicionar categoria:', error);
            throw error;
        }
    }

    /**
     * Gera relatório financeiro
     * @param {Object} params - Parâmetros do relatório
     * @returns {Promise<Object>} Dados do relatório
     */
    async generateReport(params) {
        try {
            const response = await fetch(`${this.baseUrl}/api/reports`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(params)
            });

            const result = await response.json();

            if (!result.success) {
                throw new Error(result.error);
            }

            return result.data;
        } catch (error) {
            console.error('Erro ao gerar relatório:', error);
            throw error;
        }
    }
}

/**
 * Exemplo de uso do cliente
 */
// const apiClient = new OFXApiClient('http://localhost:5000');

/**
 * Função para importar arquivo OFX no sistema financeiro
 * @param {File} file - Arquivo OFX selecionado
 * @param {Function} onSuccess - Callback de sucesso
 * @param {Function} onError - Callback de erro
 */
async function importOFXFile(file, onSuccess, onError) {
    try {
        const apiClient = new OFXApiClient();
        
        // Processar arquivo OFX
        const processedData = await apiClient.processOFXFile(file);
        
        // Adicionar transações ao sistema
        const result = await apiClient.addTransactionsBulk(processedData.transactions);
        
        if (onSuccess) {
            onSuccess({
                message: result.message,
                statistics: processedData.statistics,
                transactions: processedData.transactions
            });
        }
    } catch (error) {
        if (onError) {
            onError(error.message);
        }
    }
}

/**
 * Função para buscar transações do sistema
 * @param {Object} filters - Filtros de busca
 * @param {Function} onSuccess - Callback de sucesso
 * @param {Function} onError - Callback de erro
 */
async function getTransactions(filters = {}, onSuccess, onError) {
    try {
        const apiClient = new OFXApiClient();
        const data = await apiClient.getTransactions(filters);
        
        if (onSuccess) {
            onSuccess(data);
        }
    } catch (error) {
        if (onError) {
            onError(error.message);
        }
    }
}

/**
 * Função para buscar dados do dashboard
 * @param {Function} onSuccess - Callback de sucesso
 * @param {Function} onError - Callback de erro
 */
async function getDashboardData(onSuccess, onError) {
    try {
        const apiClient = new OFXApiClient();
        const data = await apiClient.getDashboardData();
        
        if (onSuccess) {
            onSuccess(data);
        }
    } catch (error) {
        if (onError) {
            onError(error.message);
        }
    }
}

// Exportar para uso em outros módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { OFXApiClient, importOFXFile, getTransactions, getDashboardData };
} 