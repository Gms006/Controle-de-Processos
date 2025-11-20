"""
Exportador para Excel - Versão 2 (Melhorado)
Gera planilhas com formatação profissional e análises avançadas
"""

import pandas as pd
from datetime import datetime
from pathlib import Path
import logging
import xlsxwriter


class ExportadorExcelV2:
    """Exporta dados processados para planilhas Excel com formatação avançada"""
    
    def __init__(self, output_dir: str = "output/planilhas"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def exportar_dados_brutos(self, df_geral: pd.DataFrame, df_passos: pd.DataFrame, 
                              df_desdobramentos: pd.DataFrame, nome_arquivo: str = None) -> str:
        """
        Exporta 3 abas de dados brutos para Excel com formatação profissional
        
        Args:
            df_geral: DataFrame de processos gerais
            df_passos: DataFrame de passos
            df_desdobramentos: DataFrame de desdobramentos
            nome_arquivo: Nome customizado ou None para gerar automático
        
        Returns:
            Caminho completo do arquivo gerado
        """
        if nome_arquivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"Processos_DadosBrutos_{timestamp}.xlsx"
        
        filepath = self.output_dir / nome_arquivo
        
        logging.info(f"Exportando dados para: {filepath}")
        
        # Criar writer do Excel
        with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
            workbook = writer.book
            
            # ============== FORMATOS ==============
            
            # Cabeçalho principal (azul escuro)
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#1F4E78',
                'font_color': 'white',
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
                'text_wrap': True
            })
            
            # Células normais
            cell_format = workbook.add_format({
                'border': 1,
                'align': 'left',
                'valign': 'top',
                'text_wrap': True
            })
            
            # Números
            number_format = workbook.add_format({
                'border': 1,
                'align': 'right',
                'num_format': '#,##0'
            })
            
            # Porcentagem
            percent_format = workbook.add_format({
                'border': 1,
                'align': 'center',
                'num_format': '0%'
            })
            
            # Data
            date_format = workbook.add_format({
                'border': 1,
                'align': 'center',
                'num_format': 'dd/mm/yyyy'
            })
            
            # Status - Em andamento (amarelo)
            status_andamento = workbook.add_format({
                'border': 1,
                'bg_color': '#FFF2CC',
                'font_color': '#7F6000',
                'align': 'center',
                'bold': True
            })
            
            # Status - Concluído (verde)
            status_concluido = workbook.add_format({
                'border': 1,
                'bg_color': '#C6EFCE',
                'font_color': '#006100',
                'align': 'center',
                'bold': True
            })
            
            # Status - Pendente (cinza)
            status_pendente = workbook.add_format({
                'border': 1,
                'bg_color': '#E7E6E6',
                'font_color': '#3F3F3F',
                'align': 'center'
            })
            
            # Status - OK (verde claro)
            status_ok = workbook.add_format({
                'border': 1,
                'bg_color': '#C6EFCE',
                'font_color': '#006100',
                'align': 'center',
                'bold': True
            })
            
            # ============== EXPORTAR ABAS ==============
            
            # ABA 1: PROCESSOS_GERAL
            self._exportar_aba_geral(
                df_geral, writer, workbook, header_format, cell_format, 
                number_format, date_format, percent_format,
                status_andamento, status_concluido
            )
            
            # ABA 2: PROCESSOS_PASSOS
            self._exportar_aba_passos(
                df_passos, writer, workbook, header_format, cell_format,
                number_format, status_pendente, status_ok
            )
            
            # ABA 3: PROCESSOS_DESDOBRAMENTOS
            self._exportar_aba_desdobramentos(
                df_desdobramentos, writer, workbook, header_format, cell_format,
                number_format, status_pendente
            )
        
        logging.info(f"✓ Planilha exportada com sucesso: {filepath}")
        return str(filepath)
    
    def _exportar_aba_geral(self, df, writer, workbook, header_fmt, cell_fmt, 
                           number_fmt, date_fmt, percent_fmt, status_andamento, status_concluido):
        """Exporta aba PROCESSOS_GERAL com formatação"""
        sheet_name = 'PROCESSOS_GERAL'
        
        # Escrever dados
        df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1, header=False)
        worksheet = writer.sheets[sheet_name]
        
        # Escrever cabeçalhos formatados
        for col_num, col_name in enumerate(df.columns):
            worksheet.write(0, col_num, col_name, header_fmt)
        
        # Configurar larguras de coluna
        col_widths = {
            'PROC_ID': 10,
            'EMPRESA': 40,
            'CNPJ': 18,
            'EMP_ID': 10,
            'MATRIZ_PROCESSO': 35,
            'TITULO': 35,
            'STATUS': 15,
            'PORCENTAGEM': 12,
            'DATA_INICIO': 12,
            'DATA_CONCLUSAO': 14,
            'DIAS_CORRIDOS': 14,
            'CRIADOR': 20,
            'GESTOR': 20,
            'DEPARTAMENTO': 20,
            'OBSERVACOES': 40,
            'ULTIMA_ALTERACAO': 18
        }
        
        for col_num, col_name in enumerate(df.columns):
            width = col_widths.get(col_name, 15)
            worksheet.set_column(col_num, col_num, width)
        
        # Aplicar formatação condicional para STATUS
        if 'STATUS' in df.columns:
            status_col = df.columns.get_loc('STATUS')
            for row_num in range(len(df)):
                cell_value = df.iloc[row_num]['STATUS']
                if 'andamento' in str(cell_value).lower():
                    worksheet.write(row_num + 1, status_col, cell_value, status_andamento)
                elif 'conclu' in str(cell_value).lower():
                    worksheet.write(row_num + 1, status_col, cell_value, status_concluido)
        
        # Formatar coluna PORCENTAGEM
        if 'PORCENTAGEM' in df.columns:
            porc_col = df.columns.get_loc('PORCENTAGEM')
            for row_num in range(len(df)):
                val = df.iloc[row_num]['PORCENTAGEM']
                if pd.notna(val):
                    worksheet.write(row_num + 1, porc_col, float(val)/100, percent_fmt)
        
        # Formatar colunas de DATA
        for date_col_name in ['DATA_INICIO', 'DATA_CONCLUSAO', 'ULTIMA_ALTERACAO']:
            if date_col_name in df.columns:
                col_idx = df.columns.get_loc(date_col_name)
                for row_num in range(len(df)):
                    val = df.iloc[row_num][date_col_name]
                    if pd.notna(val):
                        worksheet.write(row_num + 1, col_idx, val, date_fmt)
        
        # Formatar DIAS_CORRIDOS
        if 'DIAS_CORRIDOS' in df.columns:
            dias_col = df.columns.get_loc('DIAS_CORRIDOS')
            for row_num in range(len(df)):
                val = df.iloc[row_num]['DIAS_CORRIDOS']
                if pd.notna(val):
                    worksheet.write(row_num + 1, dias_col, val, number_fmt)
        
        # Freeze panes (primeira linha e primeiras 2 colunas)
        worksheet.freeze_panes(1, 2)
        
        # Autofilter
        worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)
    
    def _exportar_aba_passos(self, df, writer, workbook, header_fmt, cell_fmt,
                            number_fmt, status_pendente, status_ok):
        """Exporta aba PROCESSOS_PASSOS com formatação"""
        sheet_name = 'PROCESSOS_PASSOS'
        
        if df.empty:
            # Criar aba vazia com mensagem
            worksheet = workbook.add_worksheet(sheet_name)
            worksheet.write(0, 0, "Nenhum passo encontrado", cell_fmt)
            return
        
        # Escrever dados
        df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1, header=False)
        worksheet = writer.sheets[sheet_name]
        
        # Escrever cabeçalhos
        for col_num, col_name in enumerate(df.columns):
            worksheet.write(0, col_num, col_name, header_fmt)
        
        # Larguras de coluna
        col_widths = {
            'PROC_ID': 10,
            'EMPRESA': 40,
            'PASSO_ORDEM': 10,
            'PASSO_TIPO': 20,
            'PASSO_NOME': 50,
            'PASSO_STATUS': 12,
            'BLOQUEANTE': 12,
            'ENTREGA_TIPO': 15,
            'ENTREGA_NOME': 30,
            'RESPONSAVEL': 25
        }
        
        for col_num, col_name in enumerate(df.columns):
            width = col_widths.get(col_name, 15)
            worksheet.set_column(col_num, col_num, width)
        
        # Formatação condicional para PASSO_STATUS
        if 'PASSO_STATUS' in df.columns:
            status_col = df.columns.get_loc('PASSO_STATUS')
            for row_num in range(len(df)):
                cell_value = df.iloc[row_num]['PASSO_STATUS']
                if str(cell_value).lower() in ['ok', 'concluído', 'concluido']:
                    worksheet.write(row_num + 1, status_col, cell_value, status_ok)
                elif str(cell_value).lower() == 'pendente':
                    worksheet.write(row_num + 1, status_col, cell_value, status_pendente)
        
        # Freeze panes
        worksheet.freeze_panes(1, 2)
        
        # Autofilter
        worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)
    
    def _exportar_aba_desdobramentos(self, df, writer, workbook, header_fmt, 
                                    cell_fmt, number_fmt, status_pendente):
        """Exporta aba PROCESSOS_DESDOBRAMENTOS com formatação"""
        sheet_name = 'PROCESSOS_DESDOBRAMENTOS'
        
        if df.empty:
            worksheet = workbook.add_worksheet(sheet_name)
            worksheet.write(0, 0, "Nenhum desdobramento encontrado", cell_fmt)
            return
        
        # Escrever dados
        df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1, header=False)
        worksheet = writer.sheets[sheet_name]
        
        # Escrever cabeçalhos
        for col_num, col_name in enumerate(df.columns):
            worksheet.write(0, col_num, col_name, header_fmt)
        
        # Larguras de coluna
        col_widths = {
            'PROC_ID': 10,
            'EMPRESA': 40,
            'CNPJ': 18,
            'DESDOBRAMENTO_ORDEM': 12,
            'DESDOBRAMENTO_NOME': 50,
            'DESDOBRAMENTO_STATUS': 15,
            'ALTERNATIVAS_DISPONIVEIS': 40,
            'ALTERNATIVA_ESCOLHIDA': 25,
            'ACAO_TIPO': 20,
            'ACAO_NOME': 40
        }
        
        for col_num, col_name in enumerate(df.columns):
            width = col_widths.get(col_name, 15)
            worksheet.set_column(col_num, col_num, width)
        
        # Freeze panes
        worksheet.freeze_panes(1, 2)
        
        # Autofilter
        worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)
