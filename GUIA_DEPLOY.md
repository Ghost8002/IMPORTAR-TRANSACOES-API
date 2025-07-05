# 🚀 Guia Completo de Deploy - API OFX

## 🎯 Visão Geral

Este guia mostra como hospedar sua API de processamento OFX em diferentes plataformas, desde opções gratuitas até soluções empresariais.

## 📋 Pré-requisitos

1. **Conta GitHub** com seu código
2. **Arquivo OFX de teste** para validar
3. **Conhecimento básico** de Git

## 🆓 OPÇÕES GRATUITAS

### **1. Render (Recomendado para começar)**

#### **Passo a passo:**

1. **Criar conta em [render.com](https://render.com)**
2. **Conectar GitHub**
3. **Criar novo Web Service**
4. **Configurar:**

```yaml
# render.yaml (criar na raiz do projeto)
services:
  - type: web
    name: ofx-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn api_server:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
      - key: FLASK_ENV
        value: production
```

5. **Deploy automático** após push para GitHub

#### **Vantagens:**
- ✅ Gratuito (750h/mês)
- ✅ SSL automático
- ✅ Deploy automático
- ✅ Logs em tempo real

#### **URL da API:**
```
https://sua-api-ofx.onrender.com
```

### **2. Railway**

#### **Passo a passo:**

1. **Criar conta em [railway.app](https://railway.app)**
2. **Conectar GitHub**
3. **Criar novo projeto**
4. **Configurar:**

```bash
# Procfile (criar na raiz)
web: gunicorn api_server:app --bind 0.0.0.0:$PORT
```

5. **Deploy automático**

#### **Vantagens:**
- ✅ Gratuito (500h/mês)
- ✅ Deploy muito rápido
- ✅ Interface simples

### **3. Heroku**

#### **Passo a passo:**

1. **Criar conta em [heroku.com](https://heroku.com)**
2. **Instalar Heroku CLI:**
```bash
npm install -g heroku
```

3. **Configurar:**
```bash
# Login
heroku login

# Criar app
heroku create sua-api-ofx

# Configurar variáveis
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main
```

4. **Criar Procfile:**
```
web: gunicorn api_server:app
```

## 💰 OPÇÕES PAGAS

### **1. DigitalOcean App Platform**

#### **Preço:** $5-12/mês

#### **Passo a passo:**

1. **Criar conta DigitalOcean**
2. **App Platform > Create App**
3. **Conectar GitHub**
4. **Configurar:**

```yaml
# .do/app.yaml
name: ofx-api
services:
- name: web
  source_dir: /
  github:
    repo: seu-usuario/seu-repo
    branch: main
  run_command: gunicorn api_server:app
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
```

### **2. AWS Elastic Beanstalk**

#### **Preço:** $10-30/mês

#### **Passo a passo:**

1. **Criar conta AWS**
2. **Elastic Beanstalk > Create Application**
3. **Configurar:**

```python
# .ebextensions/python.config
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: api_server:app
  aws:elasticbeanstalk:application:environment:
    FLASK_ENV: production
```

### **3. Google Cloud Run**

#### **Preço:** $5-15/mês

#### **Passo a passo:**

1. **Criar projeto Google Cloud**
2. **Cloud Run > Create Service**
3. **Usar Dockerfile existente**
4. **Deploy:**

```bash
# Build e deploy
gcloud builds submit --tag gcr.io/seu-projeto/ofx-api
gcloud run deploy ofx-api --image gcr.io/seu-projeto/ofx-api --platform managed
```

## 🐳 DEPLOY COM DOCKER

### **1. Docker Local**

```bash
# Build da imagem
docker build -t ofx-api .

# Executar
docker run -p 5000:8080 ofx-api
```

### **2. Docker Compose**

```bash
# Executar com docker-compose
docker-compose up --build -d

# Ver logs
docker-compose logs -f
```

### **3. Docker Hub + VPS**

```bash
# Build e push para Docker Hub
docker build -t seu-usuario/ofx-api .
docker push seu-usuario/ofx-api

# No VPS
docker pull seu-usuario/ofx-api
docker run -d -p 80:8080 --name ofx-api seu-usuario/ofx-api
```

## 🏢 VPS (Controle Total)

### **1. DigitalOcean Droplet**

#### **Preço:** $5-10/mês

#### **Configuração manual:**

```bash
# No servidor Ubuntu
sudo apt update
sudo apt install python3 python3-pip nginx git

# Clonar projeto
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo

# Instalar dependências
pip3 install -r requirements.txt
pip3 install gunicorn

# Configurar systemd service
sudo nano /etc/systemd/system/ofx-api.service
```

```ini
[Unit]
Description=OFX API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/seu-repo
Environment="PATH=/home/ubuntu/seu-repo/venv/bin"
ExecStart=/home/ubuntu/seu-repo/venv/bin/gunicorn api_server:app --bind 0.0.0.0:5000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Ativar serviço
sudo systemctl enable ofx-api
sudo systemctl start ofx-api

# Configurar Nginx
sudo nano /etc/nginx/sites-available/ofx-api
```

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Ativar site
sudo ln -s /etc/nginx/sites-available/ofx-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 🔧 CONFIGURAÇÃO DE PRODUÇÃO

### **1. Variáveis de Ambiente**

```bash
# Configurar em produção
export FLASK_ENV=production
export SECRET_KEY=sua-chave-secreta-muito-segura
export CORS_ORIGINS=https://seusite.com,https://app.seusite.com
```

### **2. Segurança**

```python
# Adicionar no api_server.py
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

### **3. Monitoramento**

```python
# Adicionar logs estruturados
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.before_request
def log_request():
    logger.info(f"{request.method} {request.path}")
```

## 🧪 TESTE APÓS DEPLOY

### **1. Teste básico:**

```bash
# Verificar se está funcionando
curl https://sua-api.onrender.com/health

# Teste completo
python test_api.py
```

### **2. Atualizar cliente JavaScript:**

```javascript
// Atualizar URL da API
const apiClient = new OFXApiClient('https://sua-api.onrender.com');
```

## 📊 COMPARAÇÃO DE PLATAFORMAS

| Plataforma | Preço | Facilidade | Performance | Controle |
|------------|-------|------------|-------------|----------|
| Render | Gratuito | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Railway | Gratuito | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| Heroku | $7+/mês | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| DigitalOcean | $5+/mês | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| AWS | $10+/mês | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| VPS | $5+/mês | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🎯 RECOMENDAÇÃO

### **Para começar (Gratuito):**
1. **Render** - Fácil e confiável
2. **Railway** - Muito rápido

### **Para produção (Pago):**
1. **DigitalOcean App Platform** - Melhor custo-benefício
2. **Google Cloud Run** - Escalável e moderno

### **Para controle total:**
1. **VPS DigitalOcean** - $5/mês, controle completo
2. **AWS EC2** - Mais recursos, mais complexo

## 🚀 PRÓXIMOS PASSOS

1. **Escolha uma plataforma** baseada no seu orçamento
2. **Siga o guia específico** da plataforma
3. **Teste a API** após deploy
4. **Configure domínio** se necessário
5. **Monitore logs** e performance
6. **Configure backup** dos dados

A API estará pronta para uso em produção! 🎉 