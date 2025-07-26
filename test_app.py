#!/usr/bin/env python3
"""
Script de teste para validar a aplicação de dashboard de email marketing.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import tempfile
import os
import sys

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_processor import EmailDataProcessor
from visualizations import EmailVisualization

def create_sample_data():
    """Cria dados de exemplo para teste."""

    # Dados de exemplo para mapeamento
    mapping_data = {
        'Message name': [
            'E1 - Funil PV Padrão V1',
            'E2 - Funil PV Padrão V1',
            'E3 - Funil Padrão V1',
            'E4 - Funil Padrão V1',
            'E5 - Funil Padrão V1'
        ],
        'Automacao': [
            'Funil Principal',
            'Funil Principal',
            'Funil Principal',
            'Funil Principal',
            'Funil Principal'
        ]
    }

    # Dados de exemplo para uma semana
    weekly_data = {
        'Message name': [
            'E1 - Funil PV Padrão V1',
            'E2 - Funil PV Padrão V1',
            'E3 - Funil Padrão V1',
            'E4 - Funil Padrão V1',
            'E5 - Funil Padrão V1'
        ],
        'Subject': [
            'Teste 1',
            'Teste 2',
            'Teste 3',
            'Teste 4',
            'Teste 5'
        ],
        'List name': ['test_list'] * 5,
        'Sent': [100, 150, 200, 120, 180],
        'Delivered': [98, 148, 195, 118, 175],
        'Opened': [25, 30, 40, 28, 35],
        'Open rate': [0.255, 0.203, 0.205, 0.237, 0.200],
        'Clicked': [5, 8, 12, 6, 9],
        'Click rate': [0.051, 0.054, 0.062, 0.051, 0.051],
        'CTOR': [0.200, 0.267, 0.300, 0.214, 0.257],
        'Bounced': [2, 2, 5, 2, 5],
        'Bounce rate': [0.02, 0.013, 0.025, 0.017, 0.028],
        'Marked as spam': [0, 0, 0, 0, 0],
        'Spam complaint rate': [0.0, 0.0, 0.0, 0.0, 0.0],
        'Unsubscribed': [1, 0, 2, 1, 1],
        'Unsubscribe rate': [0.010, 0.0, 0.010, 0.008, 0.006],
        'Created on': [datetime.now() - timedelta(days=7)] * 5
    }

    return pd.DataFrame(mapping_data), pd.DataFrame(weekly_data)

def test_data_processor():
    """Testa o processador de dados."""
    print("🧪 Testando o processador de dados...")

    # Criar dados de exemplo
    mapping_df, weekly_df = create_sample_data()

    # Inicializar processador
    processor = EmailDataProcessor(data_dir='test_data')

    # Salvar dados em arquivos temporários
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        mapping_df.to_csv(f.name, index=False)
        mapping_file = f.name

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        weekly_df.to_csv(f.name, index=False)
        weekly_file = f.name

    try:
        # Testar carregamento de mapeamento
        processor.load_automation_mapping(mapping_file)
        print("✅ Mapeamento carregado com sucesso")

        # Testar carregamento de dados semanais
        processor.load_weekly_data(weekly_file, "Semana de Teste")
        print("✅ Dados semanais carregados com sucesso")

        # Testar análises
        summaries = processor.get_all_weeks_summary()
        print(f"✅ Resumos gerados: {len(summaries)} semanas")

        automation_metrics = processor.get_automation_performance()
        print(f"✅ Métricas de automação: {len(automation_metrics)} automações")

        # Limpeza
        os.unlink(mapping_file)
        os.unlink(weekly_file)

        return True

    except Exception as e:
        print(f"❌ Erro no teste do processador: {str(e)}")
        return False

def test_visualizations():
    """Testa as visualizações."""
    print("🧪 Testando visualizações...")

    try:
        # Inicializar visualizador
        visualizer = EmailVisualization()

        # Criar dados de exemplo
        weekly_summaries = [{
            'semana': 'Semana 1',
            'total_sent': 750,
            'total_delivered': 734,
            'total_opened': 158,
            'total_clicked': 40,
            'total_bounced': 16,
            'total_unsubscribed': 5,
            'delivery_rate': 0.979,
            'open_rate': 0.215,
            'click_rate': 0.054,
            'bounce_rate': 0.021,
            'unsubscribe_rate': 0.007,
            'ctor': 0.253
        }]

        automation_metrics = pd.DataFrame({
            'Automacao': ['Funil Principal', 'Funil Secundário'],
            'Sent': [750, 500],
            'Delivered': [734, 490],
            'Opened': [158, 98],
            'Clicked': [40, 25],
            'Bounced': [16, 10],
            'Unsubscribed': [5, 3],
            'Delivery Rate': [0.979, 0.980],
            'Open Rate': [0.215, 0.200],
            'Click Rate': [0.054, 0.051],
            'CTOR': [0.253, 0.255],
            'Bounce Rate': [0.021, 0.020],
            'Unsubscribe Rate': [0.007, 0.006]
        })

        # Testar criação de gráficos
        weekly_fig = visualizer.create_weekly_metrics_dashboard(weekly_summaries)
        print("✅ Dashboard semanal criado com sucesso")

        top_fig = visualizer.create_top_automations_chart(automation_metrics)
        print("✅ Gráfico de top automações criado com sucesso")

        overview_fig = visualizer.create_dashboard_overview(weekly_summaries, automation_metrics)
        print("✅ Dashboard de visão geral criado com sucesso")

        return True

    except Exception as e:
        print(f"❌ Erro no teste de visualizações: {str(e)}")
        return False

def test_integration():
    """Teste de integração completa."""
    print("🧪 Testando integração completa...")

    try:
        # Criar dados de exemplo
        mapping_df, weekly_df = create_sample_data()

        # Inicializar componentes
        processor = EmailDataProcessor(data_dir='test_integration')
        visualizer = EmailVisualization()

        # Salvar dados em arquivos temporários
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            mapping_df.to_csv(f.name, index=False)
            mapping_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            weekly_df.to_csv(f.name, index=False)
            weekly_file = f.name

        # Processar dados
        processor.load_automation_mapping(mapping_file)
        processor.load_weekly_data(weekly_file, "Semana de Teste")

        # Gerar análises
        summaries = processor.get_all_weeks_summary()
        automation_metrics = processor.get_automation_performance()

        # Criar visualizações
        weekly_fig = visualizer.create_weekly_metrics_dashboard(summaries)
        top_fig = visualizer.create_top_automations_chart(automation_metrics)

        # Limpeza
        os.unlink(mapping_file)
        os.unlink(weekly_file)

        print("✅ Teste de integração completo passou com sucesso")
        return True

    except Exception as e:
        print(f"❌ Erro no teste de integração: {str(e)}")
        return False

def main():
    """Executa todos os testes."""
    print("🚀 Iniciando testes da aplicação...")
    print("=" * 50)

    tests = [
        test_data_processor,
        test_visualizations,
        test_integration
    ]

    results = []
    for test in tests:
        result = test()
        results.append(result)
        print("-" * 30)

    print("=" * 50)
    print("📊 Resultados dos Testes:")
    print(f"✅ Sucessos: {sum(results)}")
    print(f"❌ Falhas: {len(results) - sum(results)}")

    if all(results):
        print("🎉 Todos os testes passaram! A aplicação está pronta para uso.")
        return True
    else:
        print("⚠️ Alguns testes falharam. Verifique os erros acima.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
