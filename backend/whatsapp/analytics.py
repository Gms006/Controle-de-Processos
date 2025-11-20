"""
Módulo de Análise e KPIs - Gestor WhatsApp
Calcula métricas gerenciais e operacionais em tempo real
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import statistics
import sys
from pathlib import Path

# Adicionar app ao path
app_path = Path(__file__).parent.parent
if str(app_path) not in sys.path:
    sys.path.insert(0, str(app_path))

from app.models import Empresa, Processo, Passo, Desdobramento
from app.database import SessionLocal


class GestorAnalytics:
    """
    Classe principal para análise de processos contábeis
    Gera KPIs e métricas para o gestor via WhatsApp
    """
    
    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db:
            self.db.close()
    
    # ============ MÉTRICAS GERAIS ============
    
    def get_resumo_geral(self, competencia: str = None) -> Dict:
        """
        Retorna resumo geral com principais KPIs
        """
        query = self.db.query(Processo)
        if competencia:
            query = query.filter(Processo.competencia == competencia)
        
        processos = query.all()
        total = len(processos)
        
        if total == 0:
            return self._resumo_vazio()
        
        # Processos por status
        concluidos = len([p for p in processos if p.status == 'Concluído'])
        em_andamento = len([p for p in processos if p.status == 'Em andamento'])
        parados = len([p for p in processos if p.porcentagem_conclusao == 0])
        
        # Progresso médio
        progresso_medio = statistics.mean([p.porcentagem_conclusao or 0 for p in processos])
        
        # Tempo médio
        dias_corridos = [p.dias_corridos for p in processos if p.dias_corridos]
        tempo_medio = statistics.mean(dias_corridos) if dias_corridos else 0
        
        # Passos
        total_passos = sum([p.total_passos or 0 for p in processos])
        passos_concluidos = sum([p.passos_concluidos or 0 for p in processos])
        passos_pendentes = total_passos - passos_concluidos
        
        # Desdobramentos
        desd_query = self.db.query(Desdobramento)
        if competencia:
            desd_query = desd_query.join(Processo).filter(Processo.competencia == competencia)
        
        total_desdobramentos = desd_query.count()
        desd_respondidos = desd_query.filter(Desdobramento.respondido == True).count()
        desd_pendentes = total_desdobramentos - desd_respondidos
        
        return {
            'total_empresas': total,
            'concluidos': concluidos,
            'em_andamento': em_andamento,
            'parados': parados,
            'taxa_conclusao': (concluidos / total * 100) if total > 0 else 0,
            'taxa_paradas': (parados / total * 100) if total > 0 else 0,
            'progresso_medio': progresso_medio,
            'tempo_medio': tempo_medio,
            'tempo_min': min(dias_corridos) if dias_corridos else 0,
            'tempo_max': max(dias_corridos) if dias_corridos else 0,
            'total_passos': total_passos,
            'passos_concluidos': passos_concluidos,
            'passos_pendentes': passos_pendentes,
            'taxa_passos': (passos_concluidos / total_passos * 100) if total_passos > 0 else 0,
            'total_desdobramentos': total_desdobramentos,
            'desd_respondidos': desd_respondidos,
            'desd_pendentes': desd_pendentes,
            'taxa_desdobramentos': (desd_respondidos / total_desdobramentos * 100) if total_desdobramentos > 0 else 0
        }
    
    def _resumo_vazio(self) -> Dict:
        """Retorna estrutura vazia quando não há dados"""
        return {
            'total_empresas': 0, 'concluidos': 0, 'em_andamento': 0, 'parados': 0,
            'taxa_conclusao': 0, 'taxa_paradas': 0, 'progresso_medio': 0,
            'tempo_medio': 0, 'tempo_min': 0, 'tempo_max': 0,
            'total_passos': 0, 'passos_concluidos': 0, 'passos_pendentes': 0, 'taxa_passos': 0,
            'total_desdobramentos': 0, 'desd_respondidos': 0, 'desd_pendentes': 0, 'taxa_desdobramentos': 0
        }
    
    # ============ ANÁLISE POR REGIME ============
    
    def get_resumo_por_regime(self, competencia: str = None) -> List[Dict]:
        """
        Retorna estatísticas agrupadas por regime tributário
        """
        query = self.db.query(Processo)
        if competencia:
            query = query.filter(Processo.competencia == competencia)
        
        processos = query.all()
        
        # Agrupar por regime
        regimes = defaultdict(list)
        for proc in processos:
            regimes[proc.regime_tributario].append(proc)
        
        resultado = []
        for regime, procs in regimes.items():
            total = len(procs)
            concluidos = len([p for p in procs if p.status == 'Concluído'])
            em_andamento = total - concluidos
            
            dias = [p.dias_corridos for p in procs if p.dias_corridos]
            tempo_medio = statistics.mean(dias) if dias else 0
            
            progresso_medio = statistics.mean([p.porcentagem_conclusao or 0 for p in procs])
            
            resultado.append({
                'regime': regime or 'Não Definido',
                'total': total,
                'concluidos': concluidos,
                'em_andamento': em_andamento,
                'taxa_conclusao': (concluidos / total * 100) if total > 0 else 0,
                'tempo_medio': tempo_medio,
                'progresso_medio': progresso_medio,
                'percentual_volume': (total / len(processos) * 100) if processos else 0
            })
        
        # Ordenar por taxa de conclusão (decrescente)
        resultado.sort(key=lambda x: x['taxa_conclusao'], reverse=True)
        
        return resultado
    
    # ============ EMPRESAS SEM FATURAMENTO ============
    
    def get_empresas_sem_faturamento(self, competencia: str = None) -> Dict:
        """
        Identifica empresas sem faturamento no período
        Baseado no desdobramento 'Houve Faturamento?'
        """
        # Buscar desdobramentos sobre faturamento
        query = self.db.query(Desdobramento).filter(
            Desdobramento.pergunta.ilike('%faturamento%')
        )
        
        if competencia:
            query = query.join(Processo).filter(Processo.competencia == competencia)
        
        desdobramentos = query.all()
        
        sem_faturamento = []
        com_faturamento = []
        pendentes = []
        
        for desd in desdobramentos:
            if not desd.respondido:
                pendentes.append(desd)
            elif desd.resposta and 'não' in desd.resposta.lower():
                sem_faturamento.append(desd)
            elif desd.resposta and 'sim' in desd.resposta.lower():
                com_faturamento.append(desd)
        
        # Buscar informações das empresas
        empresas_sem_fat = []
        for desd in sem_faturamento:
            processo = desd.processo
            empresa = processo.empresa
            
            empresas_sem_fat.append({
                'empresa_nome': empresa.nome if empresa else 'N/A',
                'cnpj': empresa.cnpj if empresa else 'N/A',
                'regime': processo.regime_tributario,
                'dias_corridos': processo.dias_corridos,
                'processo_id': processo.proc_id
            })
        
        return {
            'total_analisado': len(desdobramentos),
            'sem_faturamento': len(sem_faturamento),
            'com_faturamento': len(com_faturamento),
            'pendentes': len(pendentes),
            'taxa_sem_faturamento': (len(sem_faturamento) / len(desdobramentos) * 100) if desdobramentos else 0,
            'empresas_sem_faturamento': empresas_sem_fat,
            'tempo_medio_identificacao': statistics.mean([p['dias_corridos'] for p in empresas_sem_fat if p['dias_corridos']]) if empresas_sem_fat else 0
        }
    
    # ============ EMPRESAS COM TRIBUTOS ============
    
    def get_empresas_com_tributos(self, competencia: str = None) -> Dict:
        """
        Analisa empresas com tributos apurados
        Baseado em desdobramentos sobre ICMS, ISS, PIS/COFINS, IRPJ, CSLL, etc
        """
        tributos = {
            'PIS/COFINS': ['pis', 'cofins', 'tributos federais'],
            'IRPJ': ['irpj', 'imposto de renda'],
            'CSLL': ['csll', 'contribuição social'],
            'ICMS': ['icms'],
            'ISS': ['iss'],
            'DIFAL': ['difal', 'consumo', 'imobilizado'],
            'EFD_REINF': ['reinf', 'fato gerador'],
            'EFD_Contribuicoes': ['efd contribu'],
            'DIRB': ['dirb'],
            'MIT': ['mit']
        }
        
        resultado = {}
        
        for tributo, keywords in tributos.items():
            query = self.db.query(Desdobramento)
            
            # Filtrar por palavras-chave
            filters = [Desdobramento.pergunta.ilike(f'%{kw}%') for kw in keywords]
            query = query.filter(or_(*filters))
            
            if competencia:
                query = query.join(Processo).filter(Processo.competencia == competencia)
            
            # Contar respostas "Sim"
            desdobramentos = query.all()
            com_tributo = [d for d in desdobramentos if d.respondido and d.resposta and 'sim' in d.resposta.lower()]
            pendentes = [d for d in desdobramentos if not d.respondido]
            
            resultado[tributo] = {
                'total_perguntas': len(desdobramentos),
                'com_tributo': len(com_tributo),
                'pendentes': len(pendentes),
                'empresas': [
                    {
                        'nome': d.processo.empresa.nome if d.processo.empresa else 'N/A',
                        'cnpj': d.processo.empresa.cnpj if d.processo.empresa else 'N/A',
                        'regime': d.processo.regime_tributario
                    }
                    for d in com_tributo
                ]
            }
        
        # Total de empresas com pelo menos 1 tributo
        todas_empresas_com_tributo = set()
        for tributo_data in resultado.values():
            for emp in tributo_data['empresas']:
                todas_empresas_com_tributo.add(emp['cnpj'])
        
        return {
            'tributos': resultado,
            'total_empresas_com_tributo': len(todas_empresas_com_tributo),
            'resumo': self._gerar_resumo_tributos(resultado)
        }
    
    def _gerar_resumo_tributos(self, tributos_data: Dict) -> Dict:
        """Gera resumo consolidado de tributos"""
        return {
            tributo: {
                'quantidade': data['com_tributo'],
                'pendentes': data['pendentes']
            }
            for tributo, data in tributos_data.items()
        }
    
    # ============ DECLARAÇÕES PENDENTES ============
    
    def get_declaracoes_pendentes(self, competencia: str = None) -> Dict:
        """
        Lista declarações e obrigações acessórias pendentes
        """
        obrigacoes = {
            'DAS - Simples Nacional': {
                'regime': 'Simples Nacional',
                'prazo_dias': 20,  # Dia 20 do mês seguinte
                'criticidade': 'ALTA'
            },
            'EFD REINF': {
                'keyword': 'reinf',
                'prazo_dias': 15,
                'criticidade': 'ALTA'
            },
            'EFD Contribuições': {
                'keyword': 'efd contribu',
                'prazo_dias': 10,  # 10º dia do 2º mês seguinte
                'criticidade': 'MEDIA'
            },
            'DIFAL': {
                'keyword': 'difal',
                'prazo_dias': 9,
                'criticidade': 'MEDIA'
            },
            'DIRB': {
                'keyword': 'dirb',
                'prazo_dias': 15,  # 15 de dezembro
                'criticidade': 'BAIXA'
            },
            'MIT': {
                'keyword': 'mit',
                'prazo_dias': 20,  # 20 de dezembro
                'criticidade': 'BAIXA'
            }
        }
        
        resultado = {}
        
        for obrigacao, config in obrigacoes.items():
            if 'regime' in config:
                # Buscar por regime (ex: DAS para Simples Nacional)
                query = self.db.query(Processo).filter(
                    Processo.regime_tributario == config['regime']
                )
                if competencia:
                    query = query.filter(Processo.competencia == competencia)
                
                processos = query.all()
                total = len(processos)
                entregues = len([p for p in processos if p.status == 'Concluído'])
                pendentes = total - entregues
                
            else:
                # Buscar por desdobramento
                query = self.db.query(Desdobramento).filter(
                    Desdobramento.pergunta.ilike(f'%{config["keyword"]}%')
                )
                if competencia:
                    query = query.join(Processo).filter(Processo.competencia == competencia)
                
                desdobramentos = query.all()
                total = len(desdobramentos)
                entregues = len([d for d in desdobramentos if d.respondido and 'sim' in (d.resposta or '').lower()])
                pendentes = total - entregues
            
            resultado[obrigacao] = {
                'total': total,
                'entregues': entregues,
                'pendentes': pendentes,
                'taxa_entrega': (entregues / total * 100) if total > 0 else 0,
                'prazo_dias': config['prazo_dias'],
                'criticidade': config['criticidade']
            }
        
        return resultado
    
    # ============ TEMPO DE FINALIZAÇÃO ============
    
    def get_tempo_finalizacao(self, competencia: str = None) -> Dict:
        """
        Analisa tempo de finalização por empresa e regime
        """
        query = self.db.query(Processo).filter(Processo.status == 'Concluído')
        if competencia:
            query = query.filter(Processo.competencia == competencia)
        
        processos = query.all()
        
        if not processos:
            return {'total_concluidos': 0}
        
        # Estatísticas gerais
        dias = [p.dias_corridos for p in processos if p.dias_corridos]
        
        # Por regime
        por_regime = defaultdict(list)
        for proc in processos:
            if proc.dias_corridos:
                por_regime[proc.regime_tributario].append(proc.dias_corridos)
        
        estatisticas_regime = {}
        for regime, dias_regime in por_regime.items():
            estatisticas_regime[regime] = {
                'media': statistics.mean(dias_regime),
                'mediana': statistics.median(dias_regime),
                'minimo': min(dias_regime),
                'maximo': max(dias_regime),
                'total': len(dias_regime)
            }
        
        # Top 5 mais rápidas e mais lentas
        processos_ordenados = sorted(processos, key=lambda p: p.dias_corridos or 999)
        
        top_rapidas = [
            {
                'empresa': p.empresa.nome if p.empresa else 'N/A',
                'regime': p.regime_tributario,
                'dias': p.dias_corridos,
                'porcentagem': p.porcentagem_conclusao
            }
            for p in processos_ordenados[:5]
        ]
        
        top_lentas = [
            {
                'empresa': p.empresa.nome if p.empresa else 'N/A',
                'regime': p.regime_tributario,
                'dias': p.dias_corridos,
                'porcentagem': p.porcentagem_conclusao,
                'gargalo': self._identificar_gargalo(p)
            }
            for p in processos_ordenados[-5:][::-1]
        ]
        
        return {
            'total_concluidos': len(processos),
            'media_geral': statistics.mean(dias),
            'mediana_geral': statistics.median(dias),
            'minimo': min(dias),
            'maximo': max(dias),
            'por_regime': estatisticas_regime,
            'top_rapidas': top_rapidas,
            'top_lentas': top_lentas
        }
    
    def _identificar_gargalo(self, processo: Processo) -> str:
        """Identifica principal gargalo de um processo"""
        # Buscar passo mais demorado ou desdobramento pendente
        desdobramentos_pendentes = [d for d in processo.desdobramentos if not d.respondido]
        
        if desdobramentos_pendentes:
            return f"Desdobramento: {desdobramentos_pendentes[0].pergunta[:50]}..."
        
        return "Processamento geral"
    
    # ============ EMPRESAS PARADAS ============
    
    def get_empresas_paradas(self, competencia: str = None) -> Dict:
        """
        Identifica empresas com 0% de progresso
        """
        query = self.db.query(Processo).filter(
            and_(
                Processo.porcentagem_conclusao == 0,
                Processo.status != 'Concluído'
            )
        )
        
        if competencia:
            query = query.filter(Processo.competencia == competencia)
        
        processos_parados = query.all()
        
        # Identificar motivos de bloqueio
        empresas_paradas = []
        motivos = defaultdict(int)
        
        for proc in processos_parados:
            # Buscar primeiro desdobramento não respondido
            desd_pendente = self.db.query(Desdobramento).filter(
                and_(
                    Desdobramento.processo_id == proc.id,
                    Desdobramento.respondido == False
                )
            ).order_by(Desdobramento.ordem).first()
            
            motivo = "Aguardando " + (desd_pendente.pergunta[:30] if desd_pendente else "informações")
            motivos[motivo] += 1
            
            empresas_paradas.append({
                'empresa': proc.empresa.nome if proc.empresa else 'N/A',
                'cnpj': proc.empresa.cnpj if proc.empresa else 'N/A',
                'regime': proc.regime_tributario,
                'dias_parado': proc.dias_corridos,
                'motivo': motivo,
                'proximo_passo': desd_pendente.pergunta if desd_pendente else 'N/A'
            })
        
        # Agrupar por regime
        por_regime = defaultdict(int)
        for emp in empresas_paradas:
            por_regime[emp['regime']] += 1
        
        tempo_medio = statistics.mean([e['dias_parado'] for e in empresas_paradas if e['dias_parado']]) if empresas_paradas else 0
        
        return {
            'total_paradas': len(empresas_paradas),
            'tempo_medio_parado': tempo_medio,
            'motivos': dict(motivos),
            'por_regime': dict(por_regime),
            'empresas': empresas_paradas
        }
    
    # ============ GARGALOS POR TIPO DE PASSO ============
    
    def get_gargalos_por_passo(self, competencia: str = None) -> Dict:
        """
        Identifica gargalos por tipo de passo
        """
        query = self.db.query(Passo).filter(Passo.concluido == False)
        
        if competencia:
            query = query.join(Processo).filter(Processo.competencia == competencia)
        
        passos_pendentes = query.all()
        
        # Agrupar por nome do passo
        gargalos = defaultdict(int)
        for passo in passos_pendentes:
            gargalos[passo.nome] += 1
        
        # Ordenar por quantidade
        gargalos_ordenados = sorted(gargalos.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'total_passos_pendentes': len(passos_pendentes),
            'top_10_gargalos': [
                {'passo': nome, 'quantidade': qtd}
                for nome, qtd in gargalos_ordenados[:10]
            ]
        }
    
    # ============ DESDOBRAMENTOS NÃO RESPONDIDOS ============
    
    def get_desdobramentos_pendentes(self, competencia: str = None, top: int = 20) -> Dict:
        """
        Lista desdobramentos não respondidos
        """
        query = self.db.query(Desdobramento).filter(Desdobramento.respondido == False)
        
        if competencia:
            query = query.join(Processo).filter(Processo.competencia == competencia)
        
        desdobramentos = query.all()
        
        # Agrupar por pergunta
        perguntas = defaultdict(int)
        for desd in desdobramentos:
            perguntas[desd.pergunta] += 1
        
        # Ordenar por quantidade
        top_perguntas = sorted(perguntas.items(), key=lambda x: x[1], reverse=True)[:top]
        
        return {
            'total_pendentes': len(desdobramentos),
            'top_perguntas': [
                {'pergunta': pergunta, 'quantidade': qtd}
                for pergunta, qtd in top_perguntas
            ]
        }
    
    # ============ BUSCA POR EMPRESA ============
    
    def buscar_empresa(self, termo: str) -> List[Dict]:
        """
        Busca empresa por nome ou CNPJ
        """
        # Limpar termo
        termo_limpo = termo.strip().replace('.', '').replace('/', '').replace('-', '')
        
        # Buscar empresa
        empresas = self.db.query(Empresa).filter(
            or_(
                Empresa.nome.ilike(f'%{termo}%'),
                Empresa.cnpj.ilike(f'%{termo_limpo}%')
            )
        ).all()
        
        resultado = []
        for empresa in empresas:
            # Buscar processos da empresa
            processos = self.db.query(Processo).filter(
                Processo.empresa_id == empresa.id
            ).order_by(Processo.competencia.desc()).all()
            
            resultado.append({
                'empresa_id': empresa.id,
                'codigo': empresa.codigo,
                'nome': empresa.nome,
                'cnpj': empresa.cnpj,
                'regime': empresa.regime_tributario,
                'processos': [
                    {
                        'proc_id': p.proc_id,
                        'competencia': p.competencia,
                        'status': p.status,
                        'porcentagem': p.porcentagem_conclusao,
                        'dias_corridos': p.dias_corridos,
                        'data_inicio': p.data_inicio.isoformat() if p.data_inicio else None
                    }
                    for p in processos
                ]
            })
        
        return resultado
    
    def get_detalhes_processo(self, proc_id: int) -> Dict:
        """
        Retorna detalhes completos de um processo
        """
        processo = self.db.query(Processo).filter(Processo.proc_id == proc_id).first()
        
        if not processo:
            return None
        
        # Buscar passos
        passos = self.db.query(Passo).filter(Passo.processo_id == processo.id).all()
        
        # Buscar desdobramentos
        desdobramentos = self.db.query(Desdobramento).filter(
            Desdobramento.processo_id == processo.id
        ).all()
        
        return {
            'processo': {
                'proc_id': processo.proc_id,
                'nome': processo.nome,
                'competencia': processo.competencia,
                'status': processo.status,
                'porcentagem': processo.porcentagem_conclusao,
                'dias_corridos': processo.dias_corridos,
                'data_inicio': processo.data_inicio.isoformat() if processo.data_inicio else None,
                'regime': processo.regime_tributario
            },
            'empresa': {
                'nome': processo.empresa.nome if processo.empresa else 'N/A',
                'cnpj': processo.empresa.cnpj if processo.empresa else 'N/A',
                'codigo': processo.empresa.codigo if processo.empresa else 'N/A'
            },
            'passos': [
                {
                    'ordem': p.ordem,
                    'nome': p.nome,
                    'concluido': p.concluido,
                    'responsavel': p.responsavel
                }
                for p in sorted(passos, key=lambda x: x.ordem or 0)
            ],
            'desdobramentos': [
                {
                    'ordem': d.ordem,
                    'pergunta': d.pergunta,
                    'respondido': d.respondido,
                    'resposta': d.resposta
                }
                for d in sorted(desdobramentos, key=lambda x: x.ordem or 0)
            ]
        }


# ============ FUNÇÕES DE CONVENIÊNCIA ============

def get_resumo_geral(competencia: str = None) -> Dict:
    """Função de conveniência para resumo geral"""
    with GestorAnalytics() as analytics:
        return analytics.get_resumo_geral(competencia)


def get_resumo_por_regime(competencia: str = None) -> List[Dict]:
    """Função de conveniência para resumo por regime"""
    with GestorAnalytics() as analytics:
        return analytics.get_resumo_por_regime(competencia)


def get_empresas_sem_faturamento(competencia: str = None) -> Dict:
    """Função de conveniência para empresas sem faturamento"""
    with GestorAnalytics() as analytics:
        return analytics.get_empresas_sem_faturamento(competencia)


def buscar_empresa(termo: str) -> List[Dict]:
    """Função de conveniência para buscar empresa"""
    with GestorAnalytics() as analytics:
        return analytics.buscar_empresa(termo)


# ============ TESTE ============

if __name__ == "__main__":
    print("🔍 Testando Módulo de Análise e KPIs...\n")
    
    # Teste: Resumo Geral
    print("📊 RESUMO GERAL:")
    resumo = get_resumo_geral()
    print(f"Total de empresas: {resumo['total_empresas']}")
    print(f"Taxa de conclusão: {resumo['taxa_conclusao']:.1f}%")
    print(f"Tempo médio: {resumo['tempo_medio']:.1f} dias\n")
    
    # Teste: Por Regime
    print("📈 POR REGIME:")
    regimes = get_resumo_por_regime()
    for regime in regimes[:3]:
        print(f"  {regime['regime']}: {regime['taxa_conclusao']:.1f}% concluído")
    
    print("\n✅ Módulo de Análise OK!")
