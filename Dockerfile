# Usar imagem Python oficial
FROM python:3.9-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primeiro (para cache)
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar usuário não-root
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expor porta
EXPOSE 8080

# Variáveis de ambiente
ENV FLASK_APP=api_server.py
ENV FLASK_ENV=production
ENV PORT=8080

# Comando para iniciar a aplicação
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 api_server:app 