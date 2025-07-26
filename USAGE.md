# 📖 Exemplo de Uso

## Dados de Exemplo

Você pode usar os dados de exemplo incluídos para testar a aplicação:

```bash
# Gerar dados de demonstração
python create_demo_data.py

# Executar testes
python test_app.py

# Iniciar aplicação
./start.sh
```

## Estrutura dos Dados

### Arquivo de Mapeamento (mapeamento_automacoes.csv)
```csv
Message name,Automacao
E1 - Funil PV Padrão V1,Funil Principal
E2 - Funil PV Padrão V1,Funil Principal
Upsell - Produto A,Upsell Produtos
```

### Arquivo Semanal (Automation_messages_sent_YYYY-MM-DD.csv)
```csv
Message name,Subject,List name,Sent,Delivered,Opened,Open rate,Clicked,Click rate,CTOR,Bounced,Bounce rate,Marked as spam,Spam complaint rate,Unsubscribed,Unsubscribe rate,Created on
E1 - Funil PV Padrão V1,Teste Subject,idiomus_main,100,98,25,0.255,5,0.051,0.200,2,0.02,0,0.0,1,0.010,2022-07-15T20:15:24-03:00
```

## Funcionalidades Principais

### 1. Upload de Dados
- Faça upload do arquivo de mapeamento primeiro
- Em seguida, faça upload dos arquivos semanais
- A aplicação processará automaticamente os dados

### 2. Dashboard Principal
- Métricas gerais do período
- Visão geral das automações
- Tendências semanais

### 3. Análise Semanal
- Comparação entre semanas
- Heatmaps de performance
- Identificação de tendências

### 4. Análise de Automações
- Performance por automação
- Correlações entre métricas
- Filtros interativos

### 5. Análise de Assuntos
- Melhores assuntos por taxa de abertura/clique
- Impacto da personalização
- Análise de tamanho de assunto

## Dicas de Uso

1. **Organize seus dados:** Use nomes consistentes nos arquivos
2. **Regularidade:** Faça upload semanalmente para melhores insights
3. **Filtros:** Use os filtros para focar em dados específicos
4. **Exportação:** Exporte gráficos para relatórios
5. **Histórico:** Mantenha histórico de dados para análise temporal

## Resolução de Problemas

### Erro no Upload
- Verifique o formato do arquivo (CSV)
- Confirme se todas as colunas obrigatórias estão presentes
- Verifique a codificação do arquivo (UTF-8)

### Gráficos Vazios
- Confirme se os dados foram carregados corretamente
- Verifique se há dados suficientes para análise
- Use o botão "Recarregar Dados"

### Performance Lenta
- Reduza o período de análise
- Use filtros para limitar dados
- Limpe o cache do navegador
