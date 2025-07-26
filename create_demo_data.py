#!/usr/bin/env python3
"""
Script de demonstração para gerar dados de exemplo e testar a aplicação.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def create_demo_data():
    """Cria dados de demonstração realistas."""

    # Criar dados de mapeamento
    mapping_data = {
        'Message name': [
            'E1 - Funil PV Padrão V1 - Julho de 2022',
            'E2 - Funil PV Padrão V1 - Julho de 2022',
            'E3 - Funil Padrão V1 - Julho de 2022',
            'E4 - Funil Padrão V1 - Julho de 2022',
            'E5 - Funil Padrão V1 - Julho de 2022',
            'Upsell - Produto A',
            'Upsell - Produto B',
            'Recuperação - Carrinho 1',
            'Recuperação - Carrinho 2',
            'Newsletter - Semanal'
        ],
        'Automacao': [
            'Funil Principal',
            'Funil Principal',
            'Funil Principal',
            'Funil Principal',
            'Funil Principal',
            'Upsell Produtos',
            'Upsell Produtos',
            'Recuperação Carrinho',
            'Recuperação Carrinho',
            'Newsletter'
        ]
    }

    # Criar dados para 3 semanas
    weeks = ['2025-06-30 a 2025-07-06', '2025-07-07 a 2025-07-13', '2025-07-14 a 2025-07-20']

    all_weekly_data = []

    for week in weeks:
        # Simular variação semanal
        week_multiplier = np.random.uniform(0.8, 1.2)

        weekly_data = {
            'Message name': mapping_data['Message name'],
            'Subject': [
                '{{CONTACT `subscriber_first_name`}}?',
                'Veja isso, {{CONTACT `subscriber_first_name`}}',
                'Faça agachamento e fique fluente em inglês.',
                'From: {{CONTACT `subscriber_first_name`}} (2027)',
                'não.',
                'Oferta especial para você!',
                'Última chance - 50% OFF',
                'Você esqueceu algo...',
                'Finalize sua compra agora',
                'Newsletter semanal - Novidades'
            ],
            'List name': ['idiomus_main'] * 10,
            'Sent': np.random.randint(50, 300, 10) * week_multiplier,
            'Delivered': [],
            'Opened': [],
            'Open rate': [],
            'Clicked': [],
            'Click rate': [],
            'CTOR': [],
            'Bounced': [],
            'Bounce rate': [],
            'Marked as spam': [0] * 10,
            'Spam complaint rate': [0.0] * 10,
            'Unsubscribed': [],
            'Unsubscribe rate': [],
            'Created on': [datetime.now() - timedelta(days=7)] * 10
        }

        # Calcular métricas realistas
        for i in range(10):
            sent = int(weekly_data['Sent'][i])

            # Taxa de entrega (95-99%)
            delivered = int(sent * np.random.uniform(0.95, 0.99))

            # Taxa de abertura (10-40%)
            open_rate = np.random.uniform(0.10, 0.40)
            opened = int(delivered * open_rate)

            # Taxa de clique (1-8%)
            click_rate = np.random.uniform(0.01, 0.08)
            clicked = int(delivered * click_rate)

            # CTOR
            ctor = clicked / opened if opened > 0 else 0

            # Bounce rate (1-5%)
            bounce_rate = np.random.uniform(0.01, 0.05)
            bounced = int(sent * bounce_rate)

            # Unsubscribe rate (0.1-2%)
            unsubscribe_rate = np.random.uniform(0.001, 0.02)
            unsubscribed = int(delivered * unsubscribe_rate)

            weekly_data['Delivered'].append(delivered)
            weekly_data['Opened'].append(opened)
            weekly_data['Open rate'].append(open_rate)
            weekly_data['Clicked'].append(clicked)
            weekly_data['Click rate'].append(click_rate)
            weekly_data['CTOR'].append(ctor)
            weekly_data['Bounced'].append(bounced)
            weekly_data['Bounce rate'].append(bounce_rate)
            weekly_data['Unsubscribed'].append(unsubscribed)
            weekly_data['Unsubscribe rate'].append(unsubscribe_rate)

        all_weekly_data.append((week, pd.DataFrame(weekly_data)))

    return pd.DataFrame(mapping_data), all_weekly_data

def save_demo_files():
    """Salva arquivos de demonstração."""

    # Criar diretório de demo
    demo_dir = 'demo_data'
    os.makedirs(demo_dir, exist_ok=True)

    # Gerar dados
    mapping_df, weekly_data_list = create_demo_data()

    # Salvar mapeamento
    mapping_df.to_csv(os.path.join(demo_dir, 'mapeamento_automacoes.csv'), index=False)
    print(f"✅ Arquivo de mapeamento salvo em {demo_dir}/mapeamento_automacoes.csv")

    # Salvar dados semanais
    for week_label, weekly_df in weekly_data_list:
        filename = f"Automation_messages_sent_{week_label.replace(' a ', '').replace('-', '')}.csv"
        filepath = os.path.join(demo_dir, filename)
        weekly_df.to_csv(filepath, index=False)
        print(f"✅ Dados da semana {week_label} salvos em {filepath}")

    print(f"\n🎉 Arquivos de demonstração criados na pasta '{demo_dir}'")
    print("\n📝 Próximos passos:")
    print("1. Execute a aplicação: streamlit run app.py")
    print("2. Vá para a seção 'Upload de Dados'")
    print("3. Faça upload dos arquivos gerados")
    print("4. Explore os dashboards!")

if __name__ == "__main__":
    save_demo_files()
