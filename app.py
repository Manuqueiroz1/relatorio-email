import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import tempfile
import os

# Importar nossos módulos
from data_processor import EmailDataProcessor
from visualizations import EmailVisualization

# Configurar página
st.set_page_config(
    page_title="Dashboard de Automações de Email Marketing",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
.metric-card {
    background-color: #f0f2f6;
    border-radius: 10px;
    padding: 20px;
    margin: 10px 0;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.metric-value {
    font-size: 2.5em;
    font-weight: bold;
    color: #1f77b4;
}
.metric-label {
    font-size: 1.2em;
    color: #555;
}
.stAlert {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# Inicializar o processador de dados
@st.cache_resource
def init_data_processor():
    return EmailDataProcessor()

# Inicializar visualizações
@st.cache_resource
def init_visualizations():
    return EmailVisualization()

def main():
    st.title("📧 Dashboard de Automações de Email Marketing")
    st.markdown("---")

    # Inicializar classes
    processor = init_data_processor()
    visualizer = init_visualizations()

    # Sidebar para navegação
    st.sidebar.title("Navegação")
    page = st.sidebar.selectbox(
        "Selecione uma página:",
        ["🏠 Dashboard", "📊 Análise Semanal", "🔄 Automações", "📧 Assuntos", "📤 Upload de Dados"]
    )

    # Tentar carregar dados salvos
    if processor.load_saved_data():
        st.sidebar.success(f"Dados carregados: {len(processor.get_available_weeks())} semanas")
    else:
        st.sidebar.warning("Nenhum dado encontrado. Faça upload dos arquivos primeiro.")

    # Página de Upload de Dados
    if page == "📤 Upload de Dados":
        st.header("📤 Upload de Arquivos")

        # Instruções
        st.markdown("""
        ### Instruções de Upload
        1. **Arquivo de Mapeamento de Automações**: Upload do arquivo CSV que relaciona emails às automações
        2. **Dados Semanais**: Upload dos arquivos CSV com dados de performance semanal

        **Formato esperado para dados semanais:**
        - Arquivo CSV com colunas: Message name, Subject, List name, Sent, Delivered, Opened, Open rate, etc.
        - Nome do arquivo no formato: `Automation messages sent_YYYY-MM-DDYYYY-MM-DD.csv`
        """
        )

        # Upload do arquivo de mapeamento
        st.subheader("1. Arquivo de Mapeamento de Automações")
        mapping_file = st.file_uploader(
            "Faça upload do arquivo de mapeamento (CSV):",
            type=['csv'],
            key="mapping_file"
        )

        if mapping_file is not None:
            try:
                # Salvar arquivo temporário
                with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
                    tmp_file.write(mapping_file.getvalue())
                    tmp_path = tmp_file.name

                # Processar arquivo
                mapping_df = processor.load_automation_mapping(tmp_path)

                # Limpar arquivo temporário
                os.unlink(tmp_path)

                st.success("✅ Arquivo de mapeamento carregado com sucesso!")
                st.dataframe(mapping_df.head())

            except Exception as e:
                st.error(f"Erro ao processar arquivo de mapeamento: {str(e)}")

        # Upload dos dados semanais
        st.subheader("2. Dados Semanais")
        weekly_files = st.file_uploader(
            "Faça upload dos arquivos de dados semanais (CSV):",
            type=['csv'],
            accept_multiple_files=True,
            key="weekly_files"
        )

        if weekly_files:
            for file in weekly_files:
                try:
                    # Salvar arquivo temporário
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
                        tmp_file.write(file.getvalue())
                        tmp_path = tmp_file.name

                    # Processar arquivo
                    weekly_df = processor.load_weekly_data(tmp_path)

                    # Limpar arquivo temporário
                    os.unlink(tmp_path)

                    st.success(f"✅ Arquivo {file.name} carregado com sucesso!")

                except Exception as e:
                    st.error(f"Erro ao processar arquivo {file.name}: {str(e)}")

        # Botão para recarregar dados
        if st.button("🔄 Recarregar Dados"):
            st.cache_resource.clear()
            st.experimental_rerun()

    # Verificar se há dados para mostrar
    if not processor.get_available_weeks():
        st.warning("⚠️ Nenhum dado encontrado. Faça upload dos arquivos na seção 'Upload de Dados'.")
        return

    # Dashboard Principal
    if page == "🏠 Dashboard":
        st.header("🏠 Dashboard Principal")

        # Obter dados
        weekly_summaries = processor.get_all_weeks_summary()
        automation_metrics = processor.get_automation_performance()

        # Métricas gerais
        col1, col2, col3, col4 = st.columns(4)

        total_sent = sum([s['total_sent'] for s in weekly_summaries])
        total_opened = sum([s['total_opened'] for s in weekly_summaries])
        total_clicked = sum([s['total_clicked'] for s in weekly_summaries])
        avg_open_rate = np.mean([s['open_rate'] for s in weekly_summaries]) * 100

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_sent:,.0f}</div>
                <div class="metric-label">Emails Enviados</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_opened:,.0f}</div>
                <div class="metric-label">Emails Abertos</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_clicked:,.0f}</div>
                <div class="metric-label">Cliques</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{avg_open_rate:.2f}%</div>
                <div class="metric-label">Taxa de Abertura</div>
            </div>
            """, unsafe_allow_html=True)

        # Dashboard de visão geral
        st.subheader("📊 Visão Geral")
        overview_fig = visualizer.create_dashboard_overview(weekly_summaries, automation_metrics)
        st.plotly_chart(overview_fig, use_container_width=True)

        # Tendências semanais
        st.subheader("📈 Tendências Semanais")
        weekly_fig = visualizer.create_weekly_metrics_dashboard(weekly_summaries)
        st.plotly_chart(weekly_fig, use_container_width=True)

        # Top automações
        st.subheader("🏆 Top Automações")
        top_automations_fig = visualizer.create_top_automations_chart(automation_metrics)
        st.plotly_chart(top_automations_fig, use_container_width=True)

    # Análise Semanal
    elif page == "📊 Análise Semanal":
        st.header("📊 Análise Semanal")

        # Obter dados
        weekly_metrics = processor.get_weekly_automation_performance()
        weekly_changes = processor.get_week_over_week_changes()

        # Heatmaps semanais
        st.subheader("🔥 Heatmaps de Performance Semanal")
        heatmaps = visualizer.create_weekly_automation_heatmaps(weekly_metrics)

        for i, fig in enumerate(heatmaps):
            st.plotly_chart(fig, use_container_width=True)

        # Variações semana a semana
        st.subheader("📊 Variações Semana a Semana")
        wow_fig = visualizer.create_wow_variation_chart(weekly_changes)
        st.plotly_chart(wow_fig, use_container_width=True)

        # Tabela de dados
        st.subheader("📋 Dados Detalhados")
        st.dataframe(weekly_metrics.round(4))

    # Análise de Automações
    elif page == "🔄 Automações":
        st.header("🔄 Análise de Automações")

        # Obter dados
        automation_metrics = processor.get_automation_performance()

        # Filtros
        col1, col2 = st.columns(2)

        with col1:
            min_emails = st.slider("Número mínimo de emails enviados:", 
                                 min_value=50, max_value=5000, value=500, step=50)

        with col2:
            sort_metric = st.selectbox("Ordenar por:", 
                                     ["Sent", "Open Rate", "Click Rate", "CTOR"])

        # Filtrar dados
        filtered_data = automation_metrics[automation_metrics['Sent'] >= min_emails]
        filtered_data = filtered_data.sort_values(sort_metric, ascending=False)

        # Gráfico de barras
        st.subheader("📊 Performance das Automações")

        fig = px.bar(filtered_data.head(15), 
                    x=sort_metric, 
                    y='Automacao', 
                    orientation='h',
                    title=f'Top 15 Automações por {sort_metric}')

        st.plotly_chart(fig, use_container_width=True)

        # Matriz de correlação
        st.subheader("🔗 Matriz de Correlação")
        corr_fig = visualizer.create_correlation_matrix(filtered_data)
        st.plotly_chart(corr_fig, use_container_width=True)

        # Tabela de dados
        st.subheader("📋 Dados Detalhados")
        st.dataframe(filtered_data.round(4))

    # Análise de Assuntos
    elif page == "📧 Assuntos":
        st.header("📧 Análise de Assuntos")

        # Obter dados
        subject_metrics = processor.analyze_subject_performance()

        # Filtros
        col1, col2 = st.columns(2)

        with col1:
            min_emails = st.slider("Número mínimo de emails enviados:", 
                                 min_value=100, max_value=5000, value=1000, step=100)

        with col2:
            analysis_type = st.selectbox("Tipo de análise:", 
                                       ["Performance", "Personalização", "Tamanho"])

        # Análise de assuntos
        st.subheader("📊 Análise de Assuntos")
        subject_figs = visualizer.create_subject_analysis_charts(subject_metrics, min_emails)

        if analysis_type == "Performance":
            st.plotly_chart(subject_figs[0], use_container_width=True)  # Top abertura
            st.plotly_chart(subject_figs[1], use_container_width=True)  # Top clique
        elif analysis_type == "Personalização":
            st.plotly_chart(subject_figs[2], use_container_width=True)  # Personalização
        elif analysis_type == "Tamanho":
            st.plotly_chart(subject_figs[3], use_container_width=True)  # Tamanho

        # Análise por dia da semana
        st.subheader("📅 Performance por Dia da Semana")
        all_data = processor.combine_all_weeks()
        day_fig = visualizer.create_day_of_week_analysis(all_data)
        if day_fig:
            st.plotly_chart(day_fig, use_container_width=True)

        # Tabela de dados
        st.subheader("📋 Dados Detalhados")
        filtered_subjects = subject_metrics[subject_metrics['Sent'] >= min_emails]
        st.dataframe(filtered_subjects.round(4))

    # Informações na sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ Informações")
    st.sidebar.markdown(f"**Semanas disponíveis:** {len(processor.get_available_weeks())}")
    st.sidebar.markdown(f"**Última atualização:** {processor.metadata.get('last_updated', 'N/A')}")

    # Botão para exportar dados
    if st.sidebar.button("📥 Exportar Dados"):
        # Implementar exportação de dados
        st.sidebar.success("Funcionalidade de exportação será implementada em breve!")

if __name__ == "__main__":
    main()
