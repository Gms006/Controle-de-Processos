"""
Processador de Processos
Analisa estrutura de processos e identifica gargalos
"""

import pandas as pd
from typing import Dict, List, Tuple
from datetime import datetime
import logging


class ProcessadorProcessos:
    """Processa e analisa dados de processos"""
    
    def __init__(self):
        self.processos_concluidos = []
        self.processos_andamento = []
        self.processos_raw = []
    
    def processar_lista_processos(self, processos: List[Dict]) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Processa lista de processos e retorna 3 DataFrames
        
        Returns:
            (df_geral, df_passos, df_desdobramentos)
        """
        self.processos_raw = processos
        logging.info(f"Processando {len(processos)} processos...")
        
        # Gerar DataFrames
        df_geral = self._gerar_df_geral(processos)
        df_passos = self._gerar_df_passos(processos)
        df_desdobramentos = self._gerar_df_desdobramentos(processos)
        
        logging.info(f"Processamento concluído:")
        logging.info(f"  - Processos Geral: {len(df_geral)} linhas")
        logging.info(f"  - Passos: {len(df_passos)} linhas")
        logging.info(f"  - Desdobramentos: {len(df_desdobramentos)} linhas")
        
        return df_geral, df_passos, df_desdobramentos
    
    def _gerar_df_geral(self, processos: List[Dict]) -> pd.DataFrame:
        """Gera DataFrame da aba PROCESSOS_GERAL"""
        dados = []
        
        for proc in processos:
            row = {
                'PROC_ID': proc.get('ProcID', ''),
                'EMPRESA': proc.get('EmpNome', ''),
                'CNPJ': proc.get('EmpCNPJ', ''),
                'EMP_ID': proc.get('EmpID', ''),
                'MATRIZ_PROCESSO': proc.get('ProcNome', ''),
                'TITULO': proc.get('ProcTitulo', ''),
                'STATUS': proc.get('ProcStatus', ''),
                'PORCENTAGEM': proc.get('ProcPorcentagem', ''),
                'DATA_INICIO': self._converter_data(proc.get('ProcInicio', '')),
                'DATA_CONCLUSAO': self._converter_data(proc.get('ProcConclusao', '')),
                'DIAS_CORRIDOS': self._converter_int(proc.get('ProcDiasCorridos', 0)),
                'CRIADOR': proc.get('ProcCriador', ''),
                'GESTOR': proc.get('ProcGestor', ''),
                'DEPARTAMENTO': proc.get('ProcDepartamento', ''),
                'OBSERVACOES': proc.get('ProcObservacoes', ''),
                'ULTIMA_ALTERACAO': proc.get('DtLastDH', '')
            }
            dados.append(row)
        
        df = pd.DataFrame(dados)
        
        # Classificar processos
        if len(df) > 0:
            concluidos = df[df['STATUS'].str.contains('conclu', case=False, na=False)]
            andamento = df[df['STATUS'].str.contains('andamento', case=False, na=False)]
            
            self.processos_concluidos = concluidos.to_dict('records')
            self.processos_andamento = andamento.to_dict('records')
            
            logging.info(f"  - Concluídos: {len(concluidos)}")
            logging.info(f"  - Em andamento: {len(andamento)}")
        
        return df
    
    def _gerar_df_passos(self, processos: List[Dict]) -> pd.DataFrame:
        """Gera DataFrame da aba PROCESSOS_PASSOS"""
        dados = []
        
        for proc in processos:
            proc_id = proc.get('ProcID', '')
            empresa = proc.get('EmpNome', '')
            passos = proc.get('ProcPassos', [])
            
            if not passos:
                continue
            
            # ProcPassos é uma lista de listas: [ [passo1, passo2, ...] ]
            # Precisamos pegar o primeiro item (se existir)
            if isinstance(passos, list) and len(passos) > 0 and isinstance(passos[0], list):
                passos = passos[0]
            
            # Processar cada passo
            ordem = 1
            for passo in passos:
                rows = self._extrair_passo_recursivo(proc_id, empresa, passo, ordem)
                dados.extend(rows)
                ordem += len(rows)
        
        df = pd.DataFrame(dados)
        return df
    
    def _extrair_passo_recursivo(self, proc_id: str, empresa: str, passo: Dict, ordem: int) -> List[Dict]:
        """Extrai dados de um passo (recursivo para sub-processos)"""
        rows = []
        
        # Dados do passo atual
        tipo = passo.get('Tipo', '')
        nome = passo.get('Nome', '')
        status = passo.get('Status', '')
        automacao = passo.get('Automacao', {})
        
        # Extrair dados de automação
        bloqueante = ''
        entrega_tipo = ''
        entrega_nome = ''
        responsavel = ''
        prazo = ''
        previsao_tempo = ''
        criacao_quando = ''
        followup_quando = ''
        followup_para = ''
        
        if isinstance(automacao, dict):
            bloqueante = automacao.get('Bloqueante', '')
            
            # Entrega (para passos simples)
            entrega = automacao.get('Entrega', {})
            if isinstance(entrega, dict):
                entrega_tipo = entrega.get('Tipo', '')
                entrega_nome = entrega.get('Nome', '')
                responsavel = entrega.get('Responsavel', '')
                prazo = entrega.get('Prazo', '')
                previsao_tempo = entrega.get('Previsao', '')
                criacao_quando = entrega.get('Criacao', '')
            
            # Follow-up
            followup_quando = automacao.get('Quando', '')
            followup_para = automacao.get('Para', '')
        
        row = {
            'PROC_ID': proc_id,
            'EMPRESA': empresa,
            'PASSO_ORDEM': ordem,
            'PASSO_TIPO': tipo,
            'PASSO_NOME': nome,
            'PASSO_STATUS': status,
            'BLOQUEANTE': bloqueante,
            'ENTREGA_TIPO': entrega_tipo,
            'ENTREGA_NOME': entrega_nome,
            'RESPONSAVEL': responsavel,
            'PRAZO': prazo,
            'PREVISAO_TEMPO': previsao_tempo,
            'CRIACAO_QUANDO': criacao_quando,
            'FOLLOWUP_QUANDO': followup_quando,
            'FOLLOWUP_PARA': followup_para
        }
        rows.append(row)
        
        # Se é sub-processo, processar passos filhos recursivamente
        if tipo == 'Sub processo':
            passos_filhos = passo.get('ProcPassos', [])
            for i, passo_filho in enumerate(passos_filhos):
                rows_filhos = self._extrair_passo_recursivo(proc_id, empresa, passo_filho, ordem + i + 1)
                rows.extend(rows_filhos)
        
        return rows
    
    def _gerar_df_desdobramentos(self, processos: List[Dict]) -> pd.DataFrame:
        """Gera DataFrame da aba PROCESSOS_DESDOBRAMENTOS"""
        dados = []
        
        for proc in processos:
            proc_id = proc.get('ProcID', '')
            empresa = proc.get('EmpNome', '')
            cnpj = proc.get('EmpCNPJ', '')
            passos = proc.get('ProcPassos', [])
            
            # ProcPassos é uma lista de listas: [ [passo1, passo2, ...] ]
            # Precisamos pegar o primeiro item (se existir)
            if isinstance(passos, list) and len(passos) > 0 and isinstance(passos[0], list):
                passos = passos[0]
            
            # Buscar desdobramentos
            ordem = 1
            desdobramentos = self._encontrar_desdobramentos_recursivo(passos)
            
            for desdobramento in desdobramentos:
                nome = desdobramento.get('Nome', '')
                status = desdobramento.get('Status', '')
                automacao = desdobramento.get('Automacao', [])
                
                # Extrair alternativas
                alternativas = []
                if isinstance(automacao, list):
                    alternativas = [alt.get('Nome', '') for alt in automacao]
                
                alternativas_str = '; '.join(alternativas)
                
                # Tentar identificar qual foi escolhida (análise básica)
                alternativa_escolhida = self._identificar_escolha(desdobramento, automacao)
                
                # Ação resultante (da escolhida)
                acao_tipo = ''
                acao_nome = ''
                if alternativa_escolhida and isinstance(automacao, list):
                    for alt in automacao:
                        if alt.get('Nome') == alternativa_escolhida:
                            acao = alt.get('Acao', {})
                            if isinstance(acao, dict):
                                acao_tipo = acao.get('Tipo', '')
                                acao_nome = acao.get('Nome', '')
                            break
                
                row = {
                    'PROC_ID': proc_id,
                    'EMPRESA': empresa,
                    'CNPJ': cnpj,
                    'DESDOBRAMENTO_ORDEM': ordem,
                    'DESDOBRAMENTO_NOME': nome,
                    'DESDOBRAMENTO_STATUS': status,
                    'ALTERNATIVAS_DISPONIVEIS': alternativas_str,
                    'ALTERNATIVA_ESCOLHIDA': alternativa_escolhida,
                    'ACAO_TIPO': acao_tipo,
                    'ACAO_NOME': acao_nome
                }
                dados.append(row)
                ordem += 1
        
        df = pd.DataFrame(dados)
        return df
    
    def _encontrar_desdobramentos_recursivo(self, passos: List[Dict]) -> List[Dict]:
        """Encontra todos os desdobramentos recursivamente"""
        desdobramentos = []
        
        for passo in passos:
            tipo = passo.get('Tipo', '')
            
            if tipo == 'Desdobramento':
                desdobramentos.append(passo)
            
            # Se é sub-processo, buscar dentro dele
            if tipo == 'Sub processo':
                passos_filhos = passo.get('ProcPassos', [])
                desdobramentos.extend(self._encontrar_desdobramentos_recursivo(passos_filhos))
        
        return desdobramentos
    
    def _identificar_escolha(self, desdobramento: Dict, automacao: List) -> str:
        """
        Identifica qual alternativa foi escolhida no desdobramento
        Baseado no status e análise do fluxo
        """
        # Se status é OK e só tem uma opção, foi ela
        if desdobramento.get('Status') == 'OK' and isinstance(automacao, list):
            if len(automacao) == 1:
                return automacao[0].get('Nome', '')
            
            # Lógica para identificar baseado em padrões
            # Por ora, retorna vazio (será refinado com dados reais)
            # TODO: Implementar lógica de identificação baseada em sub-processos acionados
        
        return ''
    
    def _converter_data(self, data_str: str) -> str:
        """Converte data do formato BR para ISO (se necessário)"""
        if not data_str or data_str == '0000-00-00':
            return ''
        
        # Se já está em formato ISO, retorna
        if '-' in data_str and len(data_str) >= 10:
            return data_str
        
        # Se está em formato BR (dd/mm/yyyy), converte
        try:
            partes = data_str.split('/')
            if len(partes) == 3:
                return f"{partes[2]}-{partes[1]}-{partes[0]}"
        except:
            pass
        
        return data_str
    
    def _converter_int(self, valor) -> int:
        """Converte valor para inteiro com segurança"""
        try:
            return int(valor)
        except (ValueError, TypeError):
            return 0
    
    def gerar_estatisticas(self) -> Dict:
        """Gera estatísticas gerais dos processos"""
        stats = {
            'total_processos': len(self.processos_raw),
            'total_concluidos': len(self.processos_concluidos),
            'total_andamento': len(self.processos_andamento),
            'taxa_conclusao': 0
        }
        
        if stats['total_processos'] > 0:
            stats['taxa_conclusao'] = (stats['total_concluidos'] / stats['total_processos']) * 100
        
        return stats
