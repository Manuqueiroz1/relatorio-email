# 📧 Dashboard de Automações de Email Marketing

Uma plataforma completa em nuvem para análise de performance de automações de email marketing, construída com Streamlit.

## 🌟 Recursos

### 📊 Dashboard Principal
- Visão geral das métricas principais
- KPIs em tempo real (emails enviados, abertos, cliques, taxa de abertura)
- Resumo executivo das top automações

### 📈 Análise Semanal
- Tendências das principais métricas ao longo do tempo
- Heatmaps de performance por automação e semana
- Análise de variações semana a semana
- Identificação de tendências de crescimento ou declínio

### 🔄 Análise de Automações
- Performance detalhada por automação
- Filtros por volume mínimo de emails
- Matriz de correlação entre métricas
- Ranking por diferentes critérios

### 📧 Análise de Assuntos
- Top assuntos por taxa de abertura e clique
- Análise do impacto da personalização
- Análise do impacto do tamanho do assunto
- Performance por dia da semana

### 📤 Sistema de Upload Automatizado
- Upload de múltiplos arquivos CSV
- Processamento automático dos dados
- Armazenamento histórico
- Validação e limpeza automática dos dados

## 🚀 Como Usar

### 1. Hospedagem na Nuvem

#### Opção A: Streamlit Cloud (Recomendado)
1. Faça fork deste repositório no GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte sua conta do GitHub
4. Selecione este repositório
5. A aplicação será automaticamente hospedada

#### Opção B: Heroku
1. Instale o Heroku CLI
2. Faça login no Heroku: `heroku login`
3. Crie uma aplicação: `heroku create nome-da-sua-app`
4. Configure o buildpack: `heroku buildpacks:set heroku/python`
5. Faça deploy: `git push heroku main`

#### Opção C: Docker
```bash
# Construir a imagem
docker build -t email-dashboard .

# Executar o container
docker run -p 8501:8501 email-dashboard
```

### 2. Preparação dos Dados

#### Formato dos Arquivos Semanais:
Seus arquivos CSV semanais devem conter as seguintes colunas:
- `Message name`: Nome da mensagem
- `Subject`: Assunto do email
- `List name`: Nome da lista
- `Sent`: Número de emails enviados
- `Delivered`: Número de emails entregues
- `Opened`: Número de emails abertos
- `Open rate`: Taxa de abertura (como decimal ou porcentagem)
- `Clicked`: Número de cliques
- `Click rate`: Taxa de clique
- `CTOR`: Click-to-Open Rate
- `Bounced`: Emails rejeitados
- `Bounce rate`: Taxa de rejeição
- `Marked as spam`: Emails marcados como spam
- `Spam complaint rate`: Taxa de reclamações de spam
- `Unsubscribed`: Cancelamentos de inscrição
- `Unsubscribe rate`: Taxa de cancelamento
- `Created on`: Data de criação

#### Formato do Arquivo de Mapeamento:
- `Message name`: Nome da mensagem (deve corresponder aos arquivos semanais)
- `Automacao`: Nome da automação

### 3. Upload dos Dados

1. Acesse a seção "📤 Upload de Dados"
2. Primeiro, faça upload do arquivo de mapeamento de automações
3. Em seguida, faça upload de todos os arquivos semanais
4. A plataforma processará automaticamente os dados
5. Navegue pelas diferentes seções para visualizar as análises

## 📋 Funcionalidades Detalhadas

### Processamento Automático
- **Limpeza de Dados**: Remove caracteres especiais, converte tipos de dados
- **Validação**: Verifica integridade dos dados e consistência
- **Armazenamento**: Salva dados processados para carregamento rápido
- **Histórico**: Mantém histórico de todas as semanas carregadas

### Visualizações Interativas
- **Gráficos Plotly**: Visualizações interativas e responsivas
- **Filtros Dinâmicos**: Ajuste parâmetros em tempo real
- **Exportação**: Possibilidade de exportar gráficos e dados
- **Temas**: Interface limpa e profissional

### Análises Avançadas
- **Correlações**: Identifica relações entre métricas
- **Tendências**: Detecta padrões e tendências temporais
- **Segmentação**: Análise por diferentes critérios
- **Benchmarking**: Compara performance entre automações

## 🔧 Estrutura do Projeto

```
email_dashboard_app/
├── app.py                 # Aplicação principal Streamlit
├── data_processor.py      # Processamento de dados
├── visualizations.py      # Criação de gráficos
├── requirements.txt       # Dependências Python
├── Dockerfile            # Configuração Docker
├── README.md             # Este arquivo
└── data/                 # Diretório para dados (criado automaticamente)
```

## 🔒 Segurança e Privacidade

- Todos os dados são processados localmente na aplicação
- Não há envio de dados para serviços externos
- Armazenamento temporário seguro
- Limpeza automática de arquivos temporários

## 🛠️ Desenvolvimento Local

```bash
# Clonar o repositório
git clone [url-do-repositorio]
cd email_dashboard_app

# Instalar dependências
pip install -r requirements.txt

# Executar a aplicação
streamlit run app.py
```

## 📈 Roadmap de Funcionalidades

### ✅ Implementado
- Dashboard principal com KPIs
- Análise semanal e tendências
- Performance por automação
- Análise de assuntos
- Sistema de upload automático
- Visualizações interativas

### 🔄 Em Desenvolvimento
- Exportação de relatórios PDF
- Alertas automáticos
- API para integração
- Análise preditiva

### 📋 Planejado
- Machine Learning para otimização
- A/B Testing integration
- Notificações push
- Dashboard mobile

## 🐛 Resolução de Problemas

### Erro no Upload de Arquivos
- Verifique se o arquivo está no formato CSV
- Confirme se as colunas obrigatórias estão presentes
- Certifique-se de que os dados estão no formato correto

### Visualizações Não Aparecem
- Recarregue a página
- Verifique se os dados foram carregados corretamente
- Use o botão "🔄 Recarregar Dados"

### Performance Lenta
- Reduza o número de semanas analisadas
- Use filtros para limitar os dados
- Limpe o cache do navegador

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique este README
2. Consulte a seção de resolução de problemas
3. Entre em contato com a equipe de desenvolvimento

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para detalhes.

---

**Desenvolvido com ❤️ para otimizar suas campanhas de email marketing**
