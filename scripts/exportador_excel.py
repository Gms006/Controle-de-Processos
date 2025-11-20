"""
Exportador para Excel
Gera planilhas com análises dos processos
"""

import pandas as pd
from datetime import datetime
from pathlib import Path
import logging
import xlsxwriter


class ExportadorExcel:
    """Exporta dados processados para planilhas Excel"""
    
    def __init__(self, output_dir: str = "output/planilhas"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def exportar_dados_brutos(self, df_geral: pd.DataFrame, df_passos: pd.DataFrame, 
                              df_desdobramentos: pd.DataFrame, nome_arquivo: str = None) -> str:
        """
        Exporta 3 abas de dados brutos para Excel
        
        Args:
            df_geral: DataFrame de processos gerais
            df_passos: DataFrame de passos
            df_desdobramentos: DataFrame de desdobramentos
            nome_arquivo: Nome customizado ou None para gerar automático
        
        Returns:
            Caminho do arquivo gerado
        """
        if nome_arquivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"SimplesNacional_DadosBrutos_{timestamp}.xlsx"
        
        filepath = self.output_dir / nome_arquivo
        
        logging.info(f"Exportando dados para: {filepath}")
        
        # Criar writer do Excel
        with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
            workbook = writer.book
            
            # Definir formatos
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#4472C4',
                'font_color': 'white',
                'border': 1,
                'align': 'center',
                'valign': 'vcenter'
            })
            
            cell_format = workbook.add_format({
                'border': 1,
                'align': 'left',
                'valign': 'top',
                'text_wrap': True
            })
            
            number_format = workbook.add_format({
                'border': 1,
                'align': 'right',
                'num_format': '0'
            })
            
            date_format = workbook.add_format({
                'border': 1,
                'align': 'center',
                'num_format': 'dd/mm/yyyy'
            })
            
            # ABA 1: PROCESSOS_GERAL
            self._exportar_aba_geral(df_geral, writer, workbook, header_format, cell_format, 
                                    number_format, date_format)
            
            # ABA 2: PROCESSOS_PASSOS
            self._exportar_aba_passos(df_passos, writer, workbook, header_format, cell_format,
                                     number_format)
            
            # ABA 3: PROCESSOS_DESDOBRAMENTOS
            self._exportar_aba_desdobramentos(df_desdobramentos, writer, workbook, 
                                             header_format, cell_format)
        
        logging.info(f"✓ Planilha gerada com sucesso: {filepath}")
        logging.info(f"  - Aba 1 (PROCESSOS_GERAL): {len(df_geral)} linhas")
        logging.info(f"  - Aba 2 (PROCESSOS_PASSOS): {len(df_passos)} linhas")
        logging.info(f"  - Aba 3 (PROCESSOS_DESDOBRAMENTOS): {len(df_desdobramentos)} linhas")
        
        return str(filepath)
    
    def _exportar_aba_geral(self, df: pd.DataFrame, writer, workbook, header_format, 
                           cell_format, number_format, date_format):
        """Exporta aba PROCESSOS_GERAL com formatação"""
        sheet_name = 'PROCESSOS_GERAL'
        
        df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1, header=False)
        worksheet = writer.sheets[sheet_name]
        
        # Escrever headers com formatação
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
        
        # Ajustar largura das colunas
        column_widths = {
            'PROC_ID': 10,
            'EMPRESA': 30,
            'CNPJ': 18,
            'EMP_ID': 8,
            'MATRIZ_PROCESSO': 35,
            'TITULO': 30,
            'STATUS': 15,
            'PORCENTAGEM': 12,
            'DATA_INICIO': 12,
            'DATA_CONCLUSAO': 12,
            'DIAS_CORRIDOS': 12,
            'CRIADOR': 20,
            'GESTOR': 20,
            'DEPARTAMENTO': 15,
            'OBSERVACOES': 40,
            'ULTIMA_ALTERACAO': 18
        }
        
        for col_num, col_name in enumerate(df.columns):
            width = column_widths.get(col_name, 15)
            worksheet.set_column(col_num, col_num, width)
        
        # Congelar primeira linha (header)
        worksheet.freeze_panes(1, 0)
        
        # Adicionar filtros
        worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)
    
    def _exportar_aba_passos(self, df: pd.DataFrame, writer, workbook, header_format,
                            cell_format, number_format):
        """Exporta aba PROCESSOS_PASSOS com formatação"""
        sheet_name = 'PROCESSOS_PASSOS'
        
        df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1, header=False)
        worksheet = writer.sheets[sheet_name]
        
        # Escrever headers
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
        
        # Ajustar largura das colunas
        column_widths = {
            'PROC_ID': 10,
            'EMPRESA': 30,
            'PASSO_ORDEM': 10,
            'PASSO_TIPO': 18,
            'PASSO_NOME': 40,
            'PASSO_STATUS': 15,
            'BLOQUEANTE': 12,
            'ENTREGA_TIPO': 15,
            'ENTREGA_NOME': 30,
            'RESPONSAVEL': 20,
            'PRAZO': 12,
            'PREVISAO_TEMPO': 15,
            'CRIACAO_QUANDO': 30,
            'FOLLOWUP_QUANDO': 20,
            'FOLLOWUP_PARA': 30
        }
        
        for col_num, col_name in enumerate(df.columns):
            width = column_widths.get(col_name, 15)
            worksheet.set_column(col_num, col_num, width)
        
        worksheet.freeze_panes(1, 0)
        worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)
    
    def _exportar_aba_desdobramentos(self, df: pd.DataFrame, writer, workbook,
                                     header_format, cell_format):
        """Exporta aba PROCESSOS_DESDOBRAMENTOS com formatação"""
        sheet_name = 'PROCESSOS_DESDOBRAMENTOS'
        
        df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1, header=False)
        worksheet = writer.sheets[sheet_name]
        
        # Escrever headers
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
        
        # Ajustar largura das colunas
        column_widths = {
            'PROC_ID': 10,
            'EMPRESA': 30,
            'CNPJ': 18,
            'DESDOBRAMENTO_ORDEM': 10,
            'DESDOBRAMENTO_NOME': 40,
            'DESDOBRAMENTO_STATUS': 15,
            'ALTERNATIVAS_DISPONIVEIS': 40,
            'ALTERNATIVA_ESCOLHIDA': 25,
            'ACAO_TIPO': 20,
            'ACAO_NOME': 35
        }
        
        for col_num, col_name in enumerate(df.columns):
            width = column_widths.get(col_name, 15)
            worksheet.set_column(col_num, col_num, width)
        
        worksheet.freeze_panes(1, 0)
        worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)
    
    def exportar_processos_concluidos(self, processos: list):
        """Exporta processos concluídos para Excel (uso futuro)"""
        df = pd.DataFrame(processos)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Processos_Concluidos_{timestamp}.xlsx"
        filepath = self.output_dir / filename
        df.to_excel(filepath, index=False)
        return str(filepath)
    
    def exportar_processos_andamento(self, processos: list):
        """Exporta processos em andamento para Excel (uso futuro)"""
        df = pd.DataFrame(processos)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Processos_Andamento_{timestamp}.xlsx"
        filepath = self.output_dir / filename
        df.to_excel(filepath, index=False)
        return str(filepath)
