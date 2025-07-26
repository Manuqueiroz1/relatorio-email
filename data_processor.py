import pandas as pd
import numpy as np
import os
import datetime
import json
from typing import Dict, List, Tuple, Union, Optional
import joblib

class EmailDataProcessor:
    """
    Classe para processar dados de automações de email marketing.
    Responsável por carregar, limpar, transformar e armazenar os dados.
    """

    def __init__(self, data_dir: str = 'data'):
        """
        Inicializa o processador de dados.

        Args:
            data_dir: Diretório para armazenar os dados processados
        """
        self.data_dir = data_dir
        self.historical_data = {}
        self.mapping_data = None
        self.current_week_data = None
        self.all_weeks_data = None

        # Criar o diretório de dados se não existir
        os.makedirs(data_dir, exist_ok=True)

        # Arquivo para armazenar metadados
        self.metadata_file = os.path.join(data_dir, 'metadata.json')

        # Carregar metadados se existirem
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {
                'weeks': [],
                'last_updated': None,
                'automation_map_updated': None
            }

    def _convert_percent_to_float(self, value):
        """Converte valores percentuais para float"""
        if isinstance(value, str) and value.endswith('%'):
            return float(value.strip('%')) / 100
        return value

    def _clean_column_names(self, df):
        """Limpa os nomes das colunas"""
        df.columns = [col.strip().replace('"', '') for col in df.columns]
        return df

    def load_weekly_data(self, file_path: str, week_label: Optional[str] = None) -> pd.DataFrame:
        """
        Carrega e processa os dados semanais de automações de email.

        Args:
            file_path: Caminho para o arquivo CSV
            week_label: Rótulo para a semana (opcional). Se None, será extraído do nome do arquivo

        Returns:
            DataFrame processado
        """
        # Carregar o arquivo CSV
        df = pd.read_csv(file_path)

        # Limpar nomes de colunas
        df = self._clean_column_names(df)

        # Converter colunas de porcentagem para float
        percent_columns = ['Open rate', 'Click rate', 'CTOR', 'Bounce rate', 
                           'Spam complaint rate', 'Unsubscribe rate']

        for col in percent_columns:
            if col in df.columns:
                df[col] = df[col].apply(self._convert_percent_to_float)

        # Converter colunas numéricas
        numeric_columns = ['Sent', 'Delivered', 'Opened', 'Clicked', 'Bounced', 
                           'Marked as spam', 'Unsubscribed']

        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Converter coluna de data
        if 'Created on' in df.columns:
            df['Created on'] = pd.to_datetime(df['Created on'], errors='coerce')

        # Determinar o rótulo da semana se não fornecido
        if week_label is None:
            try:
                # Tentar extrair do nome do arquivo (formato: ...2025-MM-DD2025-MM-DD.csv)
                filename = os.path.basename(file_path)
                if 'sent_' in filename and '.csv' in filename:
                    date_part = filename.split('sent_')[1].split('.csv')[0]
                    start_date = date_part[:10]  # 2025-MM-DD
                    end_date = date_part[10:]    # 2025-MM-DD
                    week_label = f"{start_date} a {end_date}"
            except:
                # Usar a data atual como fallback
                now = datetime.datetime.now()
                week_label = f"Semana {now.isocalendar()[1]}, {now.year}"

        # Adicionar coluna de semana
        df['Semana'] = week_label

        # Armazenar no histórico
        self.current_week_data = df
        self.historical_data[week_label] = df

        # Atualizar metadados
        if week_label not in self.metadata['weeks']:
            self.metadata['weeks'].append(week_label)

        self.metadata['last_updated'] = datetime.datetime.now().isoformat()

        # Salvar metadados
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f)

        # Salvar dados da semana
        week_file = os.path.join(self.data_dir, f"week_{week_label.replace(' ', '_').replace('-', '_').replace('/', '_')}.pkl")
        df.to_pickle(week_file)

        return df

    def load_automation_mapping(self, file_path: str) -> pd.DataFrame:
        """
        Carrega o arquivo de mapeamento de automações.

        Args:
            file_path: Caminho para o arquivo CSV de mapeamento

        Returns:
            DataFrame de mapeamento processado
        """
        # Carregar o arquivo CSV
        df = pd.read_csv(file_path)

        # Limpar nomes de colunas
        df = self._clean_column_names(df)

        # Armazenar o mapeamento
        self.mapping_data = df

        # Atualizar metadados
        self.metadata['automation_map_updated'] = datetime.datetime.now().isoformat()

        # Salvar metadados
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f)

        # Salvar mapeamento
        mapping_file = os.path.join(self.data_dir, "automation_mapping.pkl")
        df.to_pickle(mapping_file)

        return df

    def merge_with_mapping(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Mescla os dados semanais com o mapeamento de automações.

        Args:
            df: DataFrame a ser mesclado. Se None, usa o atual

        Returns:
            DataFrame mesclado
        """
        if df is None:
            df = self.current_week_data

        if df is None or self.mapping_data is None:
            raise ValueError("Dados semanais ou mapeamento não carregados")

        # Mesclar baseado no nome da mensagem
        result = pd.merge(df, self.mapping_data, on='Message name', how='left')

        return result

    def combine_all_weeks(self) -> pd.DataFrame:
        """
        Combina dados de todas as semanas em um único DataFrame.

        Returns:
            DataFrame combinado
        """
        if not self.historical_data:
            raise ValueError("Nenhum dado semanal carregado")

        # Combinar todos os DataFrames
        all_data = pd.concat(list(self.historical_data.values()), ignore_index=True)

        # Armazenar os dados combinados
        self.all_weeks_data = all_data

        return all_data

    def get_available_weeks(self) -> List[str]:
        """
        Retorna a lista de semanas disponíveis.

        Returns:
            Lista de rótulos de semanas
        """
        return self.metadata['weeks']

    def load_saved_data(self) -> bool:
        """
        Carrega dados salvos anteriormente.

        Returns:
            True se os dados foram carregados com sucesso
        """
        success = True

        # Carregar mapeamento de automações
        mapping_file = os.path.join(self.data_dir, "automation_mapping.pkl")
        if os.path.exists(mapping_file):
            self.mapping_data = pd.read_pickle(mapping_file)
        else:
            success = False

        # Carregar dados de semanas
        for week in self.metadata['weeks']:
            week_file = os.path.join(self.data_dir, f"week_{week.replace(' ', '_').replace('-', '_').replace('/', '_')}.pkl")
            if os.path.exists(week_file):
                self.historical_data[week] = pd.read_pickle(week_file)
            else:
                success = False

        # Definir current_week_data para a semana mais recente
        if self.metadata['weeks']:
            latest_week = self.metadata['weeks'][-1]
            self.current_week_data = self.historical_data.get(latest_week)

        # Combinar dados de todas as semanas
        if self.historical_data:
            self.combine_all_weeks()

        return success

    def get_week_summary(self, week_label: Optional[str] = None) -> Dict:
        """
        Gera um resumo dos dados de uma semana específica.

        Args:
            week_label: Rótulo da semana. Se None, usa a semana atual

        Returns:
            Dicionário com o resumo dos dados
        """
        if week_label is None and self.current_week_data is not None:
            week_label = self.current_week_data['Semana'].iloc[0]

        if week_label is None or week_label not in self.historical_data:
            raise ValueError(f"Semana {week_label} não disponível")

        df = self.historical_data[week_label]

        # Calcular métricas gerais
        total_sent = df['Sent'].sum()
        total_delivered = df['Delivered'].sum()
        total_opened = df['Opened'].sum()
        total_clicked = df['Clicked'].sum()
        total_bounced = df['Bounced'].sum()
        total_unsubscribed = df['Unsubscribed'].sum()

        # Calcular taxas
        delivery_rate = total_delivered / total_sent if total_sent > 0 else 0
        open_rate = total_opened / total_delivered if total_delivered > 0 else 0
        click_rate = total_clicked / total_delivered if total_delivered > 0 else 0
        bounce_rate = total_bounced / total_sent if total_sent > 0 else 0
        unsubscribe_rate = total_unsubscribed / total_delivered if total_delivered > 0 else 0
        ctor = total_clicked / total_opened if total_opened > 0 else 0

        summary = {
            'semana': week_label,
            'total_sent': total_sent,
            'total_delivered': total_delivered,
            'total_opened': total_opened,
            'total_clicked': total_clicked,
            'total_bounced': total_bounced,
            'total_unsubscribed': total_unsubscribed,
            'delivery_rate': delivery_rate,
            'open_rate': open_rate,
            'click_rate': click_rate,
            'bounce_rate': bounce_rate,
            'unsubscribe_rate': unsubscribe_rate,
            'ctor': ctor
        }

        return summary

    def get_all_weeks_summary(self) -> List[Dict]:
        """
        Gera resumos para todas as semanas disponíveis.

        Returns:
            Lista de dicionários com resumos
        """
        summaries = []

        for week in self.metadata['weeks']:
            summary = self.get_week_summary(week)
            summaries.append(summary)

        return summaries

    def get_automation_performance(self, min_emails: int = 100) -> pd.DataFrame:
        """
        Analisa a performance das automações.

        Args:
            min_emails: Número mínimo de emails para incluir uma automação

        Returns:
            DataFrame com métricas por automação
        """
        if self.all_weeks_data is None:
            self.combine_all_weeks()

        if self.mapping_data is None:
            raise ValueError("Mapeamento de automações não carregado")

        # Mesclar com mapeamento
        merged_data = self.merge_with_mapping(self.all_weeks_data)

        # Agrupar por automação
        automation_metrics = merged_data.groupby('Automacao').agg({
            'Sent': 'sum',
            'Delivered': 'sum',
            'Opened': 'sum',
            'Clicked': 'sum',
            'Bounced': 'sum',
            'Unsubscribed': 'sum'
        }).reset_index()

        # Calcular taxas
        automation_metrics['Delivery Rate'] = automation_metrics['Delivered'] / automation_metrics['Sent']
        automation_metrics['Open Rate'] = automation_metrics['Opened'] / automation_metrics['Delivered']
        automation_metrics['Click Rate'] = automation_metrics['Clicked'] / automation_metrics['Delivered']
        automation_metrics['CTOR'] = automation_metrics['Clicked'] / automation_metrics['Opened']
        automation_metrics['Bounce Rate'] = automation_metrics['Bounced'] / automation_metrics['Sent']
        automation_metrics['Unsubscribe Rate'] = automation_metrics['Unsubscribed'] / automation_metrics['Delivered']

        # Filtrar por número mínimo de emails
        automation_metrics = automation_metrics[automation_metrics['Sent'] >= min_emails]

        return automation_metrics

    def get_weekly_automation_performance(self) -> pd.DataFrame:
        """
        Analisa a performance semanal das automações.

        Returns:
            DataFrame com métricas semanais por automação
        """
        if self.all_weeks_data is None:
            self.combine_all_weeks()

        if self.mapping_data is None:
            raise ValueError("Mapeamento de automações não carregado")

        # Mesclar com mapeamento
        merged_data = self.merge_with_mapping(self.all_weeks_data)

        # Agrupar por automação e semana
        weekly_metrics = merged_data.groupby(['Automacao', 'Semana']).agg({
            'Sent': 'sum',
            'Delivered': 'sum',
            'Opened': 'sum',
            'Clicked': 'sum',
            'Bounced': 'sum',
            'Unsubscribed': 'sum'
        }).reset_index()

        # Calcular taxas
        weekly_metrics['Delivery Rate'] = weekly_metrics['Delivered'] / weekly_metrics['Sent']
        weekly_metrics['Open Rate'] = weekly_metrics['Opened'] / weekly_metrics['Delivered']
        weekly_metrics['Click Rate'] = weekly_metrics['Clicked'] / weekly_metrics['Delivered']
        weekly_metrics['CTOR'] = weekly_metrics['Clicked'] / weekly_metrics['Opened']
        weekly_metrics['Bounce Rate'] = weekly_metrics['Bounced'] / weekly_metrics['Sent']
        weekly_metrics['Unsubscribe Rate'] = weekly_metrics['Unsubscribed'] / weekly_metrics['Delivered']

        return weekly_metrics

    def analyze_subject_performance(self, min_emails: int = 100) -> pd.DataFrame:
        """
        Analisa a performance dos assuntos de email.

        Args:
            min_emails: Número mínimo de emails para incluir um assunto

        Returns:
            DataFrame com métricas por assunto
        """
        if self.all_weeks_data is None:
            self.combine_all_weeks()

        # Agrupar por assunto
        subject_metrics = self.all_weeks_data.groupby('Subject').agg({
            'Sent': 'sum',
            'Delivered': 'sum',
            'Opened': 'sum',
            'Clicked': 'sum',
            'Bounced': 'sum',
            'Unsubscribed': 'sum'
        }).reset_index()

        # Calcular taxas
        subject_metrics['Delivery Rate'] = subject_metrics['Delivered'] / subject_metrics['Sent']
        subject_metrics['Open Rate'] = subject_metrics['Opened'] / subject_metrics['Delivered']
        subject_metrics['Click Rate'] = subject_metrics['Clicked'] / subject_metrics['Delivered']
        subject_metrics['CTOR'] = subject_metrics['Clicked'] / subject_metrics['Opened']
        subject_metrics['Bounce Rate'] = subject_metrics['Bounced'] / subject_metrics['Sent']
        subject_metrics['Unsubscribe Rate'] = subject_metrics['Unsubscribed'] / subject_metrics['Delivered']

        # Filtrar por número mínimo de emails
        subject_metrics = subject_metrics[subject_metrics['Sent'] >= min_emails]

        # Adicionar métricas de análise de assunto
        subject_metrics['Subject Length'] = subject_metrics['Subject'].str.len()
        subject_metrics['Has Personalization'] = subject_metrics['Subject'].str.contains('{{CONTACT') | subject_metrics['Subject'].str.contains('{{contact')
        subject_metrics['Has Question'] = subject_metrics['Subject'].str.contains('\?')
        subject_metrics['Has Number'] = subject_metrics['Subject'].str.contains('\d')

        return subject_metrics

    def get_week_over_week_changes(self) -> pd.DataFrame:
        """
        Calcula as variações semana a semana para as principais automações.

        Returns:
            DataFrame com as variações percentuais
        """
        weekly_perf = self.get_weekly_automation_performance()

        # Ordenar por semana
        weekly_perf = weekly_perf.sort_values(['Automacao', 'Semana'])

        # Calcular variações percentuais
        weekly_perf['Open Rate Change'] = weekly_perf.groupby('Automacao')['Open Rate'].pct_change() * 100
        weekly_perf['Click Rate Change'] = weekly_perf.groupby('Automacao')['Click Rate'].pct_change() * 100
        weekly_perf['CTOR Change'] = weekly_perf.groupby('Automacao')['CTOR'].pct_change() * 100

        return weekly_perf
