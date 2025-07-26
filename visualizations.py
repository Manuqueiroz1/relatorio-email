import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Optional, Union, Tuple

class EmailVisualization:
    """
    Classe para criar visualizações de dados de email marketing.
    """

    def __init__(self, theme: str = 'plotly'):
        """
        Inicializa a classe de visualização.

        Args:
            theme: Tema para os gráficos ('plotly' ou 'seaborn')
        """
        self.theme = theme
        self.color_palette = px.colors.qualitative.Plotly

        # Configurar tema seaborn
        if theme == 'seaborn':
            sns.set_theme(style="whitegrid")

    def create_weekly_metrics_dashboard(self, weekly_summaries: List[Dict]) -> go.Figure:
        """
        Cria um dashboard com as principais métricas semanais.

        Args:
            weekly_summaries: Lista de dicionários com resumos semanais

        Returns:
            Figura do Plotly
        """
        # Converter lista de dicionários para DataFrame
        df = pd.DataFrame(weekly_summaries)

        # Ordenar por semana
        df['semana_order'] = range(len(df))
        df = df.sort_values('semana_order')

        # Criar figura com subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                "Taxa de Entrega vs. Taxa de Abertura",
                "Taxa de Clique vs. CTOR",
                "Volume de Emails",
                "Taxas de Rejeição e Cancelamento"
            ),
            specs=[
                [{"type": "scatter"}, {"type": "scatter"}],
                [{"type": "bar"}, {"type": "scatter"}]
            ],
            vertical_spacing=0.15,
            horizontal_spacing=0.1
        )

        # 1. Taxa de entrega vs. Taxa de abertura
        fig.add_trace(
            go.Scatter(
                x=df['semana'],
                y=df['delivery_rate'] * 100,
                mode='lines+markers',
                name='Taxa de Entrega (%)',
                line=dict(color=self.color_palette[0], width=3),
                marker=dict(size=10)
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=df['semana'],
                y=df['open_rate'] * 100,
                mode='lines+markers',
                name='Taxa de Abertura (%)',
                line=dict(color=self.color_palette[1], width=3),
                marker=dict(size=10)
            ),
            row=1, col=1
        )

        # 2. Taxa de clique vs. CTOR
        fig.add_trace(
            go.Scatter(
                x=df['semana'],
                y=df['click_rate'] * 100,
                mode='lines+markers',
                name='Taxa de Clique (%)',
                line=dict(color=self.color_palette[2], width=3),
                marker=dict(size=10)
            ),
            row=1, col=2
        )

        fig.add_trace(
            go.Scatter(
                x=df['semana'],
                y=df['ctor'] * 100,
                mode='lines+markers',
                name='CTOR (%)',
                line=dict(color=self.color_palette[3], width=3),
                marker=dict(size=10)
            ),
            row=1, col=2
        )

        # 3. Volume de emails
        fig.add_trace(
            go.Bar(
                x=df['semana'],
                y=df['total_sent'],
                name='Emails Enviados',
                marker_color=self.color_palette[4]
            ),
            row=2, col=1
        )

        fig.add_trace(
            go.Bar(
                x=df['semana'],
                y=df['total_delivered'],
                name='Emails Entregues',
                marker_color=self.color_palette[5]
            ),
            row=2, col=1
        )

        # 4. Taxas de rejeição e cancelamento
        fig.add_trace(
            go.Scatter(
                x=df['semana'],
                y=df['bounce_rate'] * 100,
                mode='lines+markers',
                name='Taxa de Rejeição (%)',
                line=dict(color=self.color_palette[6], width=3),
                marker=dict(size=10)
            ),
            row=2, col=2
        )

        fig.add_trace(
            go.Scatter(
                x=df['semana'],
                y=df['unsubscribe_rate'] * 100,
                mode='lines+markers',
                name='Taxa de Cancelamento (%)',
                line=dict(color=self.color_palette[7], width=3),
                marker=dict(size=10)
            ),
            row=2, col=2
        )

        # Atualizar layout
        fig.update_layout(
            title_text="Tendências das Métricas de Email Marketing por Semana",
            height=800,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            ),
            template="plotly_white"
        )

        # Atualizar eixos y
        fig.update_yaxes(title_text="Porcentagem (%)", row=1, col=1)
        fig.update_yaxes(title_text="Porcentagem (%)", row=1, col=2)
        fig.update_yaxes(title_text="Quantidade", row=2, col=1)
        fig.update_yaxes(title_text="Porcentagem (%)", row=2, col=2)

        return fig

    def create_top_automations_chart(self, automation_metrics: pd.DataFrame, top_n: int = 10) -> go.Figure:
        """
        Cria um gráfico com as top automações por diferentes métricas.

        Args:
            automation_metrics: DataFrame com métricas por automação
            top_n: Número de automações a serem exibidas

        Returns:
            Figura do Plotly
        """
        # Ordenar por volume de emails enviados
        volume_sorted = automation_metrics.sort_values('Sent', ascending=False).head(top_n)

        # Criar figura com subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                "Top Automações por Taxa de Abertura",
                "Top Automações por Taxa de Clique",
                "Top Automações por CTOR",
                "Top Automações por Volume de Envio"
            ),
            specs=[
                [{"type": "bar"}, {"type": "bar"}],
                [{"type": "bar"}, {"type": "bar"}]
            ],
            vertical_spacing=0.15,
            horizontal_spacing=0.1
        )

        # 1. Top automações por taxa de abertura
        open_sorted = automation_metrics.sort_values('Open Rate', ascending=False).head(top_n)
        fig.add_trace(
            go.Bar(
                x=open_sorted['Open Rate'] * 100,
                y=open_sorted['Automacao'],
                orientation='h',
                name='Taxa de Abertura (%)',
                marker_color=self.color_palette[0]
            ),
            row=1, col=1
        )

        # 2. Top automações por taxa de clique
        click_sorted = automation_metrics.sort_values('Click Rate', ascending=False).head(top_n)
        fig.add_trace(
            go.Bar(
                x=click_sorted['Click Rate'] * 100,
                y=click_sorted['Automacao'],
                orientation='h',
                name='Taxa de Clique (%)',
                marker_color=self.color_palette[1]
            ),
            row=1, col=2
        )

        # 3. Top automações por CTOR
        ctor_sorted = automation_metrics.sort_values('CTOR', ascending=False).head(top_n)
        fig.add_trace(
            go.Bar(
                x=ctor_sorted['CTOR'] * 100,
                y=ctor_sorted['Automacao'],
                orientation='h',
                name='CTOR (%)',
                marker_color=self.color_palette[2]
            ),
            row=2, col=1
        )

        # 4. Top automações por volume
        fig.add_trace(
            go.Bar(
                x=volume_sorted['Sent'],
                y=volume_sorted['Automacao'],
                orientation='h',
                name='Emails Enviados',
                marker_color=self.color_palette[3]
            ),
            row=2, col=2
        )

        # Atualizar layout
        fig.update_layout(
            title_text="Performance das Top Automações",
            height=800,
            showlegend=False,
            template="plotly_white"
        )

        # Atualizar eixos x
        fig.update_xaxes(title_text="Taxa de Abertura (%)", row=1, col=1)
        fig.update_xaxes(title_text="Taxa de Clique (%)", row=1, col=2)
        fig.update_xaxes(title_text="CTOR (%)", row=2, col=1)
        fig.update_xaxes(title_text="Quantidade de Emails", row=2, col=2)

        return fig

    def create_weekly_automation_heatmaps(self, weekly_metrics: pd.DataFrame, top_n: int = 5) -> List[go.Figure]:
        """
        Cria heatmaps de performance semanal para as top automações.

        Args:
            weekly_metrics: DataFrame com métricas semanais por automação
            top_n: Número de automações a serem exibidas

        Returns:
            Lista de figuras do Plotly
        """
        figures = []

        # Obter as top automações por volume total
        top_automations = weekly_metrics.groupby('Automacao')['Sent'].sum().sort_values(ascending=False).head(top_n).index.tolist()

        # Filtrar apenas as top automações
        filtered_data = weekly_metrics[weekly_metrics['Automacao'].isin(top_automations)]

        # Criar pivô para taxa de abertura
        pivot_open = filtered_data.pivot(index='Automacao', columns='Semana', values='Open Rate')

        # Criar heatmap para taxa de abertura
        fig_open = go.Figure(data=go.Heatmap(
            z=pivot_open.values * 100,
            x=pivot_open.columns,
            y=pivot_open.index,
            colorscale='Blues',
            colorbar=dict(title='Taxa de Abertura (%)'),
            zmin=0,
            zmax=50
        ))

        fig_open.update_layout(
            title='Taxa de Abertura Semanal por Automação',
            xaxis_title='Semana',
            yaxis_title='Automação',
            height=500,
            template="plotly_white"
        )

        figures.append(fig_open)

        # Criar pivô para taxa de clique
        pivot_click = filtered_data.pivot(index='Automacao', columns='Semana', values='Click Rate')

        # Criar heatmap para taxa de clique
        fig_click = go.Figure(data=go.Heatmap(
            z=pivot_click.values * 100,
            x=pivot_click.columns,
            y=pivot_click.index,
            colorscale='Greens',
            colorbar=dict(title='Taxa de Clique (%)'),
            zmin=0,
            zmax=10
        ))

        fig_click.update_layout(
            title='Taxa de Clique Semanal por Automação',
            xaxis_title='Semana',
            yaxis_title='Automação',
            height=500,
            template="plotly_white"
        )

        figures.append(fig_click)

        # Criar pivô para CTOR
        pivot_ctor = filtered_data.pivot(index='Automacao', columns='Semana', values='CTOR')

        # Criar heatmap para CTOR
        fig_ctor = go.Figure(data=go.Heatmap(
            z=pivot_ctor.values * 100,
            x=pivot_ctor.columns,
            y=pivot_ctor.index,
            colorscale='Oranges',
            colorbar=dict(title='CTOR (%)'),
            zmin=0,
            zmax=30
        ))

        fig_ctor.update_layout(
            title='CTOR Semanal por Automação',
            xaxis_title='Semana',
            yaxis_title='Automação',
            height=500,
            template="plotly_white"
        )

        figures.append(fig_ctor)

        return figures

    def create_wow_variation_chart(self, weekly_changes: pd.DataFrame, top_n: int = 5) -> go.Figure:
        """
        Cria um gráfico mostrando a variação percentual semana a semana.

        Args:
            weekly_changes: DataFrame com variações semanais
            top_n: Número de automações a serem exibidas

        Returns:
            Figura do Plotly
        """
        # Obter as top automações por volume total
        top_automations = weekly_changes.groupby('Automacao')['Sent'].sum().sort_values(ascending=False).head(top_n).index.tolist()

        # Filtrar apenas as top automações e remover NaN (primeira semana)
        filtered_data = weekly_changes[weekly_changes['Automacao'].isin(top_automations)].dropna()

        # Criar figura com subplots
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=(
                "Variação da Taxa de Abertura (%)",
                "Variação da Taxa de Clique (%)"
            ),
            specs=[
                [{"type": "bar"}, {"type": "bar"}]
            ],
            horizontal_spacing=0.1
        )

        # Criar barras para variações da taxa de abertura
        for i, automacao in enumerate(top_automations):
            automacao_data = filtered_data[filtered_data['Automacao'] == automacao]

            fig.add_trace(
                go.Bar(
                    x=automacao_data['Semana'],
                    y=automacao_data['Open Rate Change'],
                    name=automacao,
                    marker_color=self.color_palette[i],
                    showlegend=True
                ),
                row=1, col=1
            )

        # Criar barras para variações da taxa de clique
        for i, automacao in enumerate(top_automations):
            automacao_data = filtered_data[filtered_data['Automacao'] == automacao]

            fig.add_trace(
                go.Bar(
                    x=automacao_data['Semana'],
                    y=automacao_data['Click Rate Change'],
                    name=automacao,
                    marker_color=self.color_palette[i],
                    showlegend=False
                ),
                row=1, col=2
            )

        # Adicionar linha de referência no zero
        fig.add_shape(
            type="line",
            x0=filtered_data['Semana'].iloc[0],
            y0=0,
            x1=filtered_data['Semana'].iloc[-1],
            y1=0,
            line=dict(color="black", width=2, dash="dash"),
            row=1, col=1
        )

        fig.add_shape(
            type="line",
            x0=filtered_data['Semana'].iloc[0],
            y0=0,
            x1=filtered_data['Semana'].iloc[-1],
            y1=0,
            line=dict(color="black", width=2, dash="dash"),
            row=1, col=2
        )

        # Atualizar layout
        fig.update_layout(
            title_text="Análise de Variação de Performance entre Semanas",
            height=500,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5
            ),
            template="plotly_white"
        )

        # Atualizar eixos
        fig.update_yaxes(title_text="Variação (%)", row=1, col=1)
        fig.update_yaxes(title_text="Variação (%)", row=1, col=2)

        return fig

    def create_subject_analysis_charts(self, subject_metrics: pd.DataFrame, min_sent: int = 1000) -> List[go.Figure]:
        """
        Cria gráficos de análise de assuntos de email.

        Args:
            subject_metrics: DataFrame com métricas por assunto
            min_sent: Número mínimo de emails enviados para incluir

        Returns:
            Lista de figuras do Plotly
        """
        figures = []

        # Filtrar por número mínimo de emails enviados
        filtered_data = subject_metrics[subject_metrics['Sent'] >= min_sent]

        # 1. Top 10 assuntos por taxa de abertura
        top_open_rate = filtered_data.sort_values('Open Rate', ascending=False).head(10)

        fig_open = go.Figure(data=go.Bar(
            x=top_open_rate['Open Rate'] * 100,
            y=top_open_rate['Subject'],
            orientation='h',
            marker_color=self.color_palette[0],
            text=top_open_rate['Sent'].apply(lambda x: f"Enviados: {x}"),
            textposition='auto'
        ))

        fig_open.update_layout(
            title='Top 10 Assuntos por Taxa de Abertura',
            xaxis_title='Taxa de Abertura (%)',
            yaxis_title='Assunto',
            height=500,
            template="plotly_white"
        )

        figures.append(fig_open)

        # 2. Top 10 assuntos por taxa de clique
        top_click_rate = filtered_data.sort_values('Click Rate', ascending=False).head(10)

        fig_click = go.Figure(data=go.Bar(
            x=top_click_rate['Click Rate'] * 100,
            y=top_click_rate['Subject'],
            orientation='h',
            marker_color=self.color_palette[1],
            text=top_click_rate['Sent'].apply(lambda x: f"Enviados: {x}"),
            textposition='auto'
        ))

        fig_click.update_layout(
            title='Top 10 Assuntos por Taxa de Clique',
            xaxis_title='Taxa de Clique (%)',
            yaxis_title='Assunto',
            height=500,
            template="plotly_white"
        )

        figures.append(fig_click)

        # 3. Análise de personalização
        personalization_analysis = filtered_data.groupby('Has Personalization').agg({
            'Open Rate': 'mean',
            'Click Rate': 'mean',
            'CTOR': 'mean',
            'Sent': 'sum'
        }).reset_index()

        personalization_analysis['Has Personalization'] = personalization_analysis['Has Personalization'].map({
            True: 'Com Personalização',
            False: 'Sem Personalização'
        })

        fig_personalization = go.Figure(data=[
            go.Bar(
                x=personalization_analysis['Has Personalization'],
                y=personalization_analysis['Open Rate'] * 100,
                name='Taxa de Abertura (%)',
                marker_color=self.color_palette[0]
            ),
            go.Bar(
                x=personalization_analysis['Has Personalization'],
                y=personalization_analysis['Click Rate'] * 100,
                name='Taxa de Clique (%)',
                marker_color=self.color_palette[1]
            ),
            go.Bar(
                x=personalization_analysis['Has Personalization'],
                y=personalization_analysis['CTOR'] * 100,
                name='CTOR (%)',
                marker_color=self.color_palette[2]
            )
        ])

        fig_personalization.update_layout(
            title='Impacto da Personalização do Assunto',
            xaxis_title='Tipo de Assunto',
            yaxis_title='Taxa (%)',
            height=500,
            template="plotly_white",
            barmode='group'
        )

        figures.append(fig_personalization)

        # 4. Análise de comprimento de assunto
        filtered_data['Subject Length Bracket'] = pd.cut(
            filtered_data['Subject Length'],
            bins=[0, 20, 40, 60, 100],
            labels=['Curto (0-20)', 'Médio (21-40)', 'Longo (41-60)', 'Muito Longo (61+)']
        )

        length_analysis = filtered_data.groupby('Subject Length Bracket').agg({
            'Open Rate': 'mean',
            'Click Rate': 'mean',
            'CTOR': 'mean',
            'Sent': 'sum'
        }).reset_index()

        fig_length = go.Figure(data=[
            go.Bar(
                x=length_analysis['Subject Length Bracket'],
                y=length_analysis['Open Rate'] * 100,
                name='Taxa de Abertura (%)',
                marker_color=self.color_palette[0]
            ),
            go.Bar(
                x=length_analysis['Subject Length Bracket'],
                y=length_analysis['Click Rate'] * 100,
                name='Taxa de Clique (%)',
                marker_color=self.color_palette[1]
            ),
            go.Bar(
                x=length_analysis['Subject Length Bracket'],
                y=length_analysis['CTOR'] * 100,
                name='CTOR (%)',
                marker_color=self.color_palette[2]
            )
        ])

        fig_length.update_layout(
            title='Impacto do Tamanho do Assunto',
            xaxis_title='Comprimento do Assunto',
            yaxis_title='Taxa (%)',
            height=500,
            template="plotly_white",
            barmode='group'
        )

        figures.append(fig_length)

        return figures

    def create_correlation_matrix(self, df: pd.DataFrame) -> go.Figure:
        """
        Cria uma matriz de correlação entre as métricas.

        Args:
            df: DataFrame com os dados

        Returns:
            Figura do Plotly
        """
        # Selecionar apenas colunas numéricas
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        # Filtrar apenas métricas relevantes
        metric_cols = [col for col in numeric_cols if any(
            term in col for term in ['rate', 'Rate', 'CTOR']
        ) and 'Change' not in col]

        if not metric_cols:
            metric_cols = numeric_cols

        # Calcular matriz de correlação
        corr_matrix = df[metric_cols].corr()

        # Criar heatmap
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu_r',
            zmin=-1,
            zmax=1,
            text=np.around(corr_matrix.values, decimals=2),
            texttemplate='%{text:.2f}'
        ))

        fig.update_layout(
            title='Matriz de Correlação entre Métricas',
            height=600,
            width=800,
            template="plotly_white"
        )

        return fig

    def create_day_of_week_analysis(self, df: pd.DataFrame) -> go.Figure:
        """
        Analisa performance por dia da semana.

        Args:
            df: DataFrame com os dados

        Returns:
            Figura do Plotly
        """
        # Verificar se a coluna de data existe
        if 'Created on' not in df.columns:
            return None

        # Extrair dia da semana
        df['Day of Week'] = df['Created on'].dt.day_name()

        # Definir ordem dos dias
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_map = {
            'Monday': 'Segunda-feira',
            'Tuesday': 'Terça-feira',
            'Wednesday': 'Quarta-feira',
            'Thursday': 'Quinta-feira',
            'Friday': 'Sexta-feira',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo'
        }

        # Traduzir dias da semana
        df['Day of Week PT'] = df['Day of Week'].map(day_map)

        # Ordenar dias da semana
        day_order_pt = [day_map[day] for day in day_order]

        # Agrupar por dia da semana
        day_analysis = df.groupby('Day of Week PT').agg({
            'Open rate': 'mean',
            'Click rate': 'mean',
            'CTOR': 'mean',
            'Sent': 'sum',
            'Delivered': 'sum',
            'Opened': 'sum',
            'Clicked': 'sum'
        }).reset_index()

        # Ordenar dias da semana
        day_analysis['Day Order'] = day_analysis['Day of Week PT'].map({day: i for i, day in enumerate(day_order_pt)})
        day_analysis = day_analysis.sort_values('Day Order')

        # Criar figura com subplots
        fig = make_subplots(
            rows=1, cols=3,
            subplot_titles=(
                "Taxa de Abertura por Dia da Semana",
                "Taxa de Clique por Dia da Semana",
                "Volume de Envio por Dia da Semana"
            ),
            specs=[
                [{"type": "bar"}, {"type": "bar"}, {"type": "bar"}]
            ],
            horizontal_spacing=0.1
        )

        # 1. Taxa de abertura por dia da semana
        fig.add_trace(
            go.Bar(
                x=day_analysis['Day of Week PT'],
                y=day_analysis['Open rate'] * 100,
                marker_color=self.color_palette[0],
                showlegend=False
            ),
            row=1, col=1
        )

        # 2. Taxa de clique por dia da semana
        fig.add_trace(
            go.Bar(
                x=day_analysis['Day of Week PT'],
                y=day_analysis['Click rate'] * 100,
                marker_color=self.color_palette[1],
                showlegend=False
            ),
            row=1, col=2
        )

        # 3. Volume de envio por dia da semana
        fig.add_trace(
            go.Bar(
                x=day_analysis['Day of Week PT'],
                y=day_analysis['Sent'],
                marker_color=self.color_palette[2],
                showlegend=False
            ),
            row=1, col=3
        )

        # Atualizar layout
        fig.update_layout(
            title_text="Desempenho por Dia da Semana",
            height=500,
            template="plotly_white"
        )

        # Atualizar eixos
        fig.update_yaxes(title_text="Taxa de Abertura (%)", row=1, col=1)
        fig.update_yaxes(title_text="Taxa de Clique (%)", row=1, col=2)
        fig.update_yaxes(title_text="Quantidade de Emails", row=1, col=3)

        return fig

    def create_dashboard_overview(self, weekly_summaries: List[Dict], automation_metrics: pd.DataFrame) -> go.Figure:
        """
        Cria um dashboard de visão geral com os principais indicadores.

        Args:
            weekly_summaries: Lista de dicionários com resumos semanais
            automation_metrics: DataFrame com métricas por automação

        Returns:
            Figura do Plotly
        """
        # Converter lista de dicionários para DataFrame
        df_weekly = pd.DataFrame(weekly_summaries)

        # Calcular médias gerais
        avg_open_rate = df_weekly['open_rate'].mean() * 100
        avg_click_rate = df_weekly['click_rate'].mean() * 100
        avg_ctor = df_weekly['ctor'].mean() * 100
        total_sent = df_weekly['total_sent'].sum()
        total_opened = df_weekly['total_opened'].sum()
        total_clicked = df_weekly['total_clicked'].sum()

        # Obter a semana mais recente e a mais antiga
        latest_week = df_weekly.iloc[-1]['semana']
        oldest_week = df_weekly.iloc[0]['semana']

        # Calcular tendências (última semana vs. primeira semana)
        open_rate_trend = (df_weekly.iloc[-1]['open_rate'] / df_weekly.iloc[0]['open_rate'] - 1) * 100
        click_rate_trend = (df_weekly.iloc[-1]['click_rate'] / df_weekly.iloc[0]['click_rate'] - 1) * 100

        # Obter as top 3 automações por taxa de abertura e taxa de clique
        top_open = automation_metrics.sort_values('Open Rate', ascending=False).head(3)
        top_click = automation_metrics.sort_values('Click Rate', ascending=False).head(3)

        # Criar figura para o dashboard
        fig = go.Figure()

        # Adicionar texto de visão geral
        fig.add_annotation(
            text=f"<b>Dashboard de Performance de Email Marketing</b><br><br>"
                 f"<b>Período de Análise:</b> {oldest_week} a {latest_week}<br>"
                 f"<b>Total de Emails Enviados:</b> {total_sent:,.0f}<br>"
                 f"<b>Total de Aberturas:</b> {total_opened:,.0f}<br>"
                 f"<b>Total de Cliques:</b> {total_clicked:,.0f}<br><br>"
                 f"<b>Taxa Média de Abertura:</b> {avg_open_rate:.2f}% ({'+' if open_rate_trend >= 0 else ''}{open_rate_trend:.2f}%)<br>"
                 f"<b>Taxa Média de Clique:</b> {avg_click_rate:.2f}% ({'+' if click_rate_trend >= 0 else ''}{click_rate_trend:.2f}%)<br>"
                 f"<b>CTOR Médio:</b> {avg_ctor:.2f}%<br><br>"
                 f"<b>Top 3 Automações por Taxa de Abertura:</b><br>"
                 f"1. {top_open.iloc[0]['Automacao']} - {top_open.iloc[0]['Open Rate']*100:.2f}%<br>"
                 f"2. {top_open.iloc[1]['Automacao']} - {top_open.iloc[1]['Open Rate']*100:.2f}%<br>"
                 f"3. {top_open.iloc[2]['Automacao']} - {top_open.iloc[2]['Open Rate']*100:.2f}%<br><br>"
                 f"<b>Top 3 Automações por Taxa de Clique:</b><br>"
                 f"1. {top_click.iloc[0]['Automacao']} - {top_click.iloc[0]['Click Rate']*100:.2f}%<br>"
                 f"2. {top_click.iloc[1]['Automacao']} - {top_click.iloc[1]['Click Rate']*100:.2f}%<br>"
                 f"3. {top_click.iloc[2]['Automacao']} - {top_click.iloc[2]['Click Rate']*100:.2f}%",
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            align="center",
            font=dict(size=16)
        )

        # Atualizar layout
        fig.update_layout(
            height=600,
            template="plotly_white"
        )

        return fig
