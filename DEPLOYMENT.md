# 🚀 Guia de Deploy

## Opções de Hospedagem

### 1. Streamlit Cloud (Recomendado - Gratuito)

1. **Preparar o repositório:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/seu-usuario/email-dashboard.git
   git push -u origin main
   ```

2. **Deploy:**
   - Acesse https://share.streamlit.io/
   - Conecte sua conta do GitHub
   - Selecione o repositório
   - Confirme o arquivo principal: `app.py`
   - A aplicação será automaticamente implantada

### 2. Heroku

1. **Preparar arquivos:**
   ```bash
   echo "web: streamlit run app.py --server.port=$PORT --server.headless=true" > Procfile
   ```

2. **Deploy:**
   ```bash
   heroku create nome-da-sua-app
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

### 3. Railway

1. **Configurar railway.json:**
   ```json
   {
     "deploy": {
       "startCommand": "streamlit run app.py --server.port=$PORT --server.headless=true"
     }
   }
   ```

2. **Deploy:**
   - Conecte seu GitHub ao Railway
   - Selecione o repositório
   - Configure as variáveis de ambiente
   - Deploy automático

### 4. Docker + Cloud Provider

1. **Construir imagem:**
   ```bash
   docker build -t email-dashboard .
   ```

2. **Deploy para AWS/GCP/Azure:**
   - Use o Dockerfile incluído
   - Configure load balancer
   - Expor porta 8501

### 5. Render

1. **Configurar render.yaml:**
   ```yaml
   services:
     - type: web
       name: email-dashboard
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: streamlit run app.py --server.port=$PORT --server.headless=true
   ```

## Configurações Importantes

### Variáveis de Ambiente
```bash
PORT=8501
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_PORT=8501
```

### Configurações de Memória
- Mínimo: 512MB RAM
- Recomendado: 1GB+ RAM
- Para grandes datasets: 2GB+ RAM

### Configurações de Rede
- Porta padrão: 8501
- Protocolo: HTTP/HTTPS
- Timeout: 30 segundos

## Troubleshooting

### Erro de Memória
- Reduzir tamanho dos dados
- Usar cache do Streamlit
- Otimizar visualizações

### Erro de Permissão
- Verificar permissões de arquivo
- Configurar usuário correto no Docker

### Erro de Port
- Verificar se a porta está sendo usada
- Configurar PORT environment variable
