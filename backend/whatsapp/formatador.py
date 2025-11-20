"""
Módulo de Formatação de Relatórios para WhatsApp
Gera mensagens formatadas, otimizadas para mobile
"""

from typing import Dict, List
from datetime import datetime


class WhatsAppFormatter:
    """
    Classe para formatação de relatórios para WhatsApp
    Otimizado para visualização mobile com emojis e símbolos
    """
    
    # Símbolos e emojis
    SEPARADOR = "━" * 39
    SEPARADOR_FINO = "─" * 39
    BOX_TOP = "╔" + "═" * 37 + "╗"
    BOX_BOTTOM = "╚" + "═" * 37 + "╝"
    
    @staticmethod
    def box_title(titulo: str) -> str:
        """Cria título em caixa"""
        padding = (37 - len(titulo)) // 2
        linha = " " * padding + titulo + " " * padding
        if len(linha) < 37:
            linha += " "
        return f"╔{'═' * 37}╗\n║{linha}║\n╚{'═' * 37}╝"
    
    @staticmethod
    def barra_progresso(percentual: float, tamanho: int = 10) -> str:
        """Gera barra de progresso ASCII"""
        blocos_cheios = int(percentual / 100 * tamanho)
        blocos_vazios = tamanho - blocos_cheios
        return "▓" * blocos_cheios + "░" * blocos_vazios
    
    @staticmethod
    def status_emoji(percentual: float) -> str:
        """Retorna emoji baseado no percentual"""
        if percentual >= 75:
            return "🟢"
        elif percentual >= 50:
            return "🟡"
        elif percentual >= 25:
            return "🟠"
        else:
            return "🔴"
    
    @staticmethod
    def criticidade_emoji(criticidade: str) -> str:
        """Retorna emoji de criticidade"""
        mapa = {
            'ALTA': '🔴',
            'MEDIA': '🟡',
            'BAIXA': '🟢'
        }
        return mapa.get(criticidade, '⚪')
    
    # ============ MENU PRINCIPAL ============
    
    @classmethod
    def menu_principal(cls) -> str:
        """Gera menu principal de comandos"""
        return f"""
{cls.box_title("🤖 GESTOR DE PROCESSOS CONTÁBEIS")}
       Competência: 10/2025

📊 RESUMOS EXECUTIVOS
{cls.SEPARADOR}
1️⃣ Resumo Geral (KPIs principais)
2️⃣ Resumo por Regime Tributário
3️⃣ Resumo por Empresa

🔍 ANÁLISES ESPECÍFICAS
{cls.SEPARADOR}
4️⃣ Empresas sem Faturamento
5️⃣ Empresas com Tributos Apurados
6️⃣ Declarações Pendentes
7️⃣ Declarações Dispensadas

⏱️ DESEMPENHO E PRODUTIVIDADE
{cls.SEPARADOR}
8️⃣ Tempo de Finalização por Empresa
9️⃣ Processos Atrasados/Críticos
🔟 Top 10 Empresas Mais Rápidas
1️⃣1️⃣ Top 10 Empresas Mais Lentas

🚨 ALERTAS E GARGALOS
{cls.SEPARADOR}
1️⃣2️⃣ Empresas Paradas (0% progresso)
1️⃣3️⃣ Gargalos por Tipo de Passo
1️⃣4️⃣ Desdobramentos Não Respondidos
1️⃣5️⃣ Obrigações Acessórias Pendentes

📈 INDICADORES GERENCIAIS
{cls.SEPARADOR}
1️⃣6️⃣ Taxa de Conclusão Geral
1️⃣7️⃣ Média de Dias por Regime
1️⃣8️⃣ Análise de Faturamento (REINF)
1️⃣9️⃣ Análise de DIRB/MIT/EFD

🔎 CONSULTAS PERSONALIZADAS
{cls.SEPARADOR}
2️⃣0️⃣ Buscar por Nome da Empresa
2️⃣1️⃣ Buscar por CNPJ
2️⃣2️⃣ Filtrar por Status

⚙️ CONFIGURAÇÕES
{cls.SEPARADOR}
2️⃣3️⃣ Ajuda (Lista de Comandos)
2️⃣4️⃣ Sobre o Sistema

{cls.SEPARADOR}
💡 Digite o número ou palavra-chave
   Ex: "1" ou "resumo geral"
"""
    
    # ============ RESUMO GERAL ============
    
    @classmethod
    def resumo_geral(cls, dados: Dict) -> str:
        """Formata resumo geral"""
        return f"""
{cls.box_title("📊 RESUMO GERAL - 10/2025")}

🏢 EMPRESAS
{cls.SEPARADOR}
Total: {dados['total_empresas']} empresas
✅ Concluídas: {dados['concluidos']} ({dados['taxa_conclusao']:.1f}%)
⏳ Em Andamento: {dados['em_andamento']} ({100-dados['taxa_conclusao']:.1f}%)
🛑 Paradas (0%): {dados['parados']} empresas ({dados['taxa_paradas']:.1f}%)

📈 PROGRESSO MÉDIO
{cls.SEPARADOR}
Geral: {cls.barra_progresso(dados['progresso_medio'])} {dados['progresso_medio']:.1f}%

⏱️ TEMPO MÉDIO
{cls.SEPARADOR}
Dias corridos: {dados['tempo_medio']:.1f} dias
Mínimo: {dados['tempo_min']} dias
Máximo: {dados['tempo_max']} dias
Meta mensal: 30 dias
Status: {cls.status_emoji(100 - (dados['tempo_medio']/30*100))} {'Dentro do prazo' if dados['tempo_medio'] <= 30 else 'Atrasado'}

🎯 PASSOS
{cls.SEPARADOR}
Total: {dados['total_passos']:,} passos
✅ Concluídos: {dados['passos_concluidos']:,} ({dados['taxa_passos']:.1f}%)
⏳ Pendentes: {dados['passos_pendentes']:,} ({100-dados['taxa_passos']:.1f}%)

❓ DESDOBRAMENTOS
{cls.SEPARADOR}
Total: {dados['total_desdobramentos']} perguntas
✅ Respondidos: {dados['desd_respondidos']} ({dados['taxa_desdobramentos']:.1f}%)
⏳ Pendentes: {dados['desd_pendentes']} ({100-dados['taxa_desdobramentos']:.1f}%)

🚨 ALERTAS CRÍTICOS
{cls.SEPARADOR}
🔴 {dados['desd_pendentes']} desdobramentos pendentes
   ({100-dados['taxa_desdobramentos']:.1f}% aguardando resposta)

{f"🟡 {dados['parados']} empresas paradas" if dados['parados'] > 0 else ""}
   {f"sem nenhum progresso" if dados['parados'] > 0 else ""}

{cls.SEPARADOR}
✅ Próximas Ações:
1. Coletar informações pendentes
2. Desbloquear empresas paradas
3. Acelerar processos lentos
{cls.SEPARADOR}

Digite outro número ou 0 para menu
"""
    
    # ============ RESUMO POR REGIME ============
    
    @classmethod
    def resumo_por_regime(cls, dados: List[Dict]) -> str:
        """Formata resumo por regime tributário"""
        linhas = [
            cls.box_title("📊 ANÁLISE POR REGIME - 10/2025"),
            ""
        ]
        
        # Emojis por regime
        emoji_regime = {
            'Simples Nacional': '🟢',
            'Lucro Presumido': '🔵',
            'Lucro Real': '🟣'
        }
        
        for regime_data in dados:
            regime = regime_data['regime']
            emoji = '🟢' if 'Simples' in regime else '🔵' if 'Presumido' in regime else '🟣'
            
            # Status baseado na taxa de conclusão
            if regime_data['taxa_conclusao'] >= 50:
                status = "🟢 EXCELENTE"
            elif regime_data['taxa_conclusao'] >= 25:
                status = "🟡 REGULAR"
            else:
                status = "🔴 CRÍTICO"
            
            linhas.extend([
                f"{emoji} {regime.upper()}",
                cls.SEPARADOR,
                f"Empresas: {regime_data['total']} ({regime_data['percentual_volume']:.1f}% do total)",
                f"Concluídos: {regime_data['concluidos']} ({regime_data['taxa_conclusao']:.1f}%) {cls.status_emoji(regime_data['taxa_conclusao'])}",
                f"Em Andamento: {regime_data['em_andamento']} ({100-regime_data['taxa_conclusao']:.1f}%)",
                f"Dias Médios: {regime_data['tempo_medio']:.1f} dias",
                f"Progresso: {cls.barra_progresso(regime_data['progresso_medio'])} {regime_data['progresso_medio']:.1f}%",
                f"Status: {status}",
                ""
            ])
        
        # Ranking
        linhas.extend([
            cls.SEPARADOR,
            "🎯 Ranking de Desempenho:",
            ""
        ])
        
        ranking = sorted(dados, key=lambda x: x['taxa_conclusao'], reverse=True)
        for i, regime_data in enumerate(ranking, 1):
            linhas.append(f"{i}º {regime_data['regime']} ({regime_data['taxa_conclusao']:.1f}%)")
        
        linhas.extend([
            cls.SEPARADOR,
            "",
            "Digite outro número ou 0 para menu"
        ])
        
        return "\n".join(linhas)
    
    # ============ EMPRESAS SEM FATURAMENTO ============
    
    @classmethod
    def empresas_sem_faturamento(cls, dados: Dict) -> str:
        """Formata lista de empresas sem faturamento"""
        linhas = [
            cls.box_title("🔍 EMPRESAS SEM FATURAMENTO"),
            "        Competência: 10/2025",
            "",
            "📊 VISÃO GERAL",
            cls.SEPARADOR,
            f"Total Analisado: {dados['total_analisado']} empresas",
            f"Sem Faturamento: {dados['sem_faturamento']} empresas ({dados['taxa_sem_faturamento']:.1f}%)",
            f"Com Faturamento: {dados['com_faturamento']} empresas",
            "",
            "❓ AGUARDANDO RESPOSTA",
            cls.SEPARADOR,
            f"Desdobramento 'Faturamento':",
            f"{dados['pendentes']} empresas pendentes ({dados['pendentes']/dados['total_analisado']*100 if dados['total_analisado'] > 0 else 0:.1f}%)",
            ""
        ]
        
        if dados['empresas_sem_faturamento']:
            linhas.extend([
                "📋 LISTA - EMPRESAS SEM FATURAMENTO",
                cls.SEPARADOR,
                ""
            ])
            
            for i, emp in enumerate(dados['empresas_sem_faturamento'][:10], 1):
                linhas.extend([
                    f"{i}. {emp['empresa_nome'][:30]}",
                    f"   CNPJ: {emp['cnpj']}",
                    f"   Regime: {emp['regime']}",
                    f"   Status: Dispensado de Declarações",
                    f"   Dias: {emp['dias_corridos']} dias",
                    ""
                ])
            
            if len(dados['empresas_sem_faturamento']) > 10:
                linhas.append(f"... e mais {len(dados['empresas_sem_faturamento']) - 10} empresas")
                linhas.append("")
        
        linhas.extend([
            cls.SEPARADOR,
            f"📈 IMPACTO NO FATURAMENTO:",
            f"• {dados['taxa_sem_faturamento']:.1f}% das empresas sem movimento",
            f"• Média de {dados['tempo_medio_identificacao']:.1f} dias para identificar",
            f"• {dados['pendentes']} empresas aguardando confirmação",
            "",
            "✅ Ações Recomendadas:",
            "1. Acelerar coleta de info faturamento",
            "2. Validar empresas inativas",
            "3. Dispensar declarações desnecessárias",
            cls.SEPARADOR,
            "",
            "Digite outro número ou 0 para menu"
        ])
        
        return "\n".join(linhas)
    
    # ============ EMPRESAS COM TRIBUTOS ============
    
    @classmethod
    def empresas_com_tributos(cls, dados: Dict) -> str:
        """Formata análise de tributos"""
        resumo = dados['resumo']
        
        linhas = [
            cls.box_title("💰 EMPRESAS COM TRIBUTOS"),
            "        Competência: 10/2025",
            "",
            "📊 RESUMO DE APURAÇÃO",
            cls.SEPARADOR,
            f"Total de Empresas: {dados['total_empresas_com_tributo']}",
            "",
            "💵 TRIBUTOS FEDERAIS",
            cls.SEPARADOR
        ]
        
        # Tributos Federais
        for tributo in ['PIS/COFINS', 'IRPJ', 'CSLL', 'EFD_Contribuicoes']:
            if tributo in resumo:
                linhas.append(f"{tributo.replace('_', ' ')}: {resumo[tributo]['quantidade']} empresas")
        
        linhas.extend([
            "",
            "🏛️ TRIBUTOS ESTADUAIS",
            cls.SEPARADOR
        ])
        
        # Tributos Estaduais
        for tributo in ['ICMS', 'DIFAL']:
            if tributo in resumo:
                linhas.append(f"{tributo}: {resumo[tributo]['quantidade']} empresas")
        
        linhas.extend([
            "",
            "🏙️ TRIBUTOS MUNICIPAIS",
            cls.SEPARADOR
        ])
        
        # Tributos Municipais
        if 'ISS' in resumo:
            linhas.append(f"ISS: {resumo['ISS']['quantidade']} empresas")
        
        linhas.extend([
            "",
            "📋 OBRIGAÇÕES ACESSÓRIAS",
            cls.SEPARADOR
        ])
        
        # Obrigações Acessórias
        for tributo in ['EFD_REINF', 'DIRB', 'MIT']:
            if tributo in resumo:
                pendentes = resumo[tributo]['pendentes']
                linhas.append(f"{tributo.replace('_', ' ')}: {pendentes} empresas pendentes")
        
        linhas.extend([
            "",
            cls.SEPARADOR,
            "✅ Próximas Ações:",
            f"1. Conferir guias geradas",
            f"2. Validar obrigações pendentes",
            f"3. Confirmar obrigatoriedades",
            cls.SEPARADOR,
            "",
            "Digite outro número ou 0 para menu"
        ])
        
        return "\n".join(linhas)
    
    # ============ DECLARAÇÕES PENDENTES ============
    
    @classmethod
    def declaracoes_pendentes(cls, dados: Dict) -> str:
        """Formata declarações pendentes"""
        linhas = [
            cls.box_title("📋 DECLARAÇÕES PENDENTES"),
            "        Competência: 10/2025",
            ""
        ]
        
        # Separar por criticidade
        criticas = {k: v for k, v in dados.items() if v.get('criticidade') == 'ALTA'}
        regulares = {k: v for k, v in dados.items() if v.get('criticidade') == 'MEDIA'}
        em_dia = {k: v for k, v in dados.items() if v.get('criticidade') == 'BAIXA'}
        
        # Obrigações Críticas
        if criticas:
            linhas.extend([
                "🔴 OBRIGAÇÕES CRÍTICAS (Prazo curto)",
                cls.SEPARADOR
            ])
            
            for obrigacao, info in criticas.items():
                # Calcular data de vencimento (aproximada)
                prazo = info['prazo_dias']
                
                linhas.extend([
                    f"{obrigacao}",
                    f"📅 Prazo: ~{prazo} dias",
                    f"Empresas: {info['total']}",
                    f"Status: {cls.status_emoji(info['taxa_entrega'])} {info['entregues']} entregues ({info['taxa_entrega']:.1f}%)",
                    f"Pendentes: {info['pendentes']} empresas {'⚠️' if info['pendentes'] > 0 else ''}",
                    ""
                ])
        
        # Obrigações Regulares
        if regulares:
            linhas.extend([
                "🟡 OBRIGAÇÕES REGULARES",
                cls.SEPARADOR
            ])
            
            for obrigacao, info in regulares.items():
                linhas.extend([
                    f"{obrigacao}",
                    f"📅 Prazo: ~{info['prazo_dias']} dias",
                    f"Empresas: {info['total']}",
                    f"Status: {cls.status_emoji(info['taxa_entrega'])} {info['entregues']} entregues ({info['taxa_entrega']:.1f}%)",
                    f"Pendentes: {info['pendentes']} empresas",
                    ""
                ])
        
        # Obrigações Em Dia
        if em_dia:
            linhas.extend([
                "🟢 OBRIGAÇÕES EM DIA",
                cls.SEPARADOR
            ])
            
            for obrigacao, info in em_dia.items():
                linhas.extend([
                    f"{obrigacao}",
                    f"📅 Prazo: ~{info['prazo_dias']} dias",
                    f"Empresas: {info['total']}",
                    f"Status: {cls.status_emoji(info['taxa_entrega'])} {info['entregues']} entregues ({info['taxa_entrega']:.1f}%)",
                    f"Pendentes: {info['pendentes']} empresas",
                    ""
                ])
        
        # Urgências
        urgencias = []
        for obrigacao, info in dados.items():
            if info['criticidade'] == 'ALTA' and info['pendentes'] > 0:
                urgencias.append(f"{cls.criticidade_emoji(info['criticidade'])} {obrigacao} - {info['pendentes']} emp")
        
        if urgencias:
            linhas.extend([
                cls.SEPARADOR,
                "⚠️ URGÊNCIAS:",
                *[f"{i+1}. {urg}" for i, urg in enumerate(urgencias)],
                cls.SEPARADOR
            ])
        
        linhas.extend([
            "",
            "Digite outro número ou 0 para menu"
        ])
        
        return "\n".join(linhas)
    
    # ============ TEMPO DE FINALIZAÇÃO ============
    
    @classmethod
    def tempo_finalizacao(cls, dados: Dict) -> str:
        """Formata análise de tempo de finalização"""
        if dados.get('total_concluidos', 0) == 0:
            return "⚠️ Nenhum processo concluído ainda.\n\nDigite outro número ou 0 para menu"
        
        linhas = [
            cls.box_title("⏱️ TEMPO DE FINALIZAÇÃO"),
            "        Competência: 10/2025",
            "",
            "📊 ESTATÍSTICAS GERAIS",
            cls.SEPARADOR,
            f"Empresas Concluídas: {dados['total_concluidos']}",
            f"Média Geral: {dados['media_geral']:.1f} dias",
            f"Mediana: {dados['mediana_geral']:.1f} dias",
            f"Mínimo: {dados['minimo']} dias",
            f"Máximo: {dados['maximo']} dias",
            "",
            "📈 POR REGIME TRIBUTÁRIO",
            cls.SEPARADOR
        ]
        
        # Estatísticas por regime
        for regime, stats in dados['por_regime'].items():
            linhas.extend([
                f"{regime}:",
                f"  Média: {stats['media']:.1f} dias {cls.status_emoji(100 - stats['media']/30*100)}",
                f"  Empresas: {stats['total']} concluídas",
                ""
            ])
        
        # Top 5 Rápidas
        if dados.get('top_rapidas'):
            linhas.extend([
                "🏆 TOP 5 - MAIS RÁPIDAS",
                cls.SEPARADOR
            ])
            
            for i, emp in enumerate(dados['top_rapidas'], 1):
                linhas.extend([
                    f"{i}. {emp['empresa'][:30]}",
                    f"   Regime: {emp['regime']}",
                    f"   ⏱️ {emp['dias']} dias | ✅ {emp['porcentagem']:.0f}%",
                    ""
                ])
        
        # Top 5 Lentas
        if dados.get('top_lentas'):
            linhas.extend([
                "🐌 TOP 5 - MAIS LENTAS",
                cls.SEPARADOR
            ])
            
            for i, emp in enumerate(dados['top_lentas'], 1):
                linhas.extend([
                    f"{i}. {emp['empresa'][:30]}",
                    f"   Regime: {emp['regime']}",
                    f"   ⏱️ {emp['dias']} dias | ✅ {emp['porcentagem']:.0f}%",
                    f"   Gargalo: {emp['gargalo'][:35]}",
                    ""
                ])
        
        # Insight
        if dados['por_regime']:
            regimes_list = list(dados['por_regime'].items())
            mais_rapido = min(regimes_list, key=lambda x: x[1]['media'])
            mais_lento = max(regimes_list, key=lambda x: x[1]['media'])
            
            dif_percent = ((mais_lento[1]['media'] - mais_rapido[1]['media']) / mais_rapido[1]['media'] * 100)
            
            linhas.extend([
                cls.SEPARADOR,
                "💡 Insight:",
                f"• {mais_rapido[0]} {dif_percent:.0f}% mais rápido",
                f"• {mais_lento[0]} {dif_percent:.0f}% mais lento",
                cls.SEPARADOR
            ])
        
        linhas.extend([
            "",
            "Digite outro número ou 0 para menu"
        ])
        
        return "\n".join(linhas)
    
    # ============ EMPRESAS PARADAS ============
    
    @classmethod
    def empresas_paradas(cls, dados: Dict) -> str:
        """Formata lista de empresas paradas"""
        linhas = [
            cls.box_title("🛑 EMPRESAS PARADAS (0% progresso)"),
            "        Competência: 10/2025",
            "",
            "⚠️ SITUAÇÃO CRÍTICA",
            cls.SEPARADOR,
            f"Total de Empresas Paradas: {dados['total_paradas']} ({dados['total_paradas']/211*100:.1f}%)",
            f"Tempo Médio Paradas: {dados['tempo_medio_parado']:.1f} dias",
            f"Impacto: {cls.status_emoji(100 - dados['total_paradas']/211*100)} {'BAIXO' if dados['total_paradas'] < 20 else 'MÉDIO' if dados['total_paradas'] < 40 else 'ALTO'}",
            "",
            "📋 MOTIVOS DE BLOQUEIO",
            cls.SEPARADOR
        ]
        
        # Motivos
        for motivo, qtd in dados['motivos'].items():
            linhas.append(f"{motivo}: {qtd} empresas")
        
        # Por regime
        linhas.extend([
            "",
            "📊 POR REGIME",
            cls.SEPARADOR
        ])
        
        for regime, qtd in dados['por_regime'].items():
            pct = qtd / dados['total_paradas'] * 100 if dados['total_paradas'] > 0 else 0
            linhas.append(f"{regime}: {qtd} empresas ({pct:.1f}%)")
        
        # Lista de empresas
        if dados.get('empresas'):
            linhas.extend([
                "",
                "🔴 LISTA - EMPRESAS PARADAS",
                cls.SEPARADOR,
                ""
            ])
            
            for i, emp in enumerate(dados['empresas'][:10], 1):
                linhas.extend([
                    f"{i}. {emp['empresa'][:30]}",
                    f"   CNPJ: {emp['cnpj']}",
                    f"   Regime: {emp['regime']}",
                    f"   Parada há: {emp['dias_parado']} dias",
                    f"   Bloqueio: {emp['motivo'][:35]}",
                    f"   Próximo: {emp['proximo_passo'][:35]}",
                    ""
                ])
            
            if len(dados['empresas']) > 10:
                linhas.append(f"... e mais {len(dados['empresas']) - 10} empresas\n")
        
        linhas.extend([
            cls.SEPARADOR,
            "✅ Ações Urgentes:",
            f"1. Coletar informações pendentes",
            f"2. Validar dados com empresas",
            f"3. Liberar processos bloqueados",
            "",
            "🎯 Meta: Reduzir para <5% em 7 dias",
            cls.SEPARADOR,
            "",
            "Digite outro número ou 0 para menu"
        ])
        
        return "\n".join(linhas)
    
    # ============ DETALHES DE EMPRESA ============
    
    @classmethod
    def detalhes_empresa(cls, dados: Dict) -> str:
        """Formata detalhes de uma empresa específica"""
        proc = dados['processo']
        emp = dados['empresa']
        
        linhas = [
            cls.SEPARADOR,
            "📋 RESULTADO DA BUSCA",
            cls.SEPARADOR,
            "",
            f"🏢 {emp['nome']}",
            f"CNPJ: {emp['cnpj']}",
            f"Código: {emp['codigo']}",
            "",
            "📊 PROCESSO ATUAL",
            cls.SEPARADOR,
            f"Processo: {proc['nome']}",
            f"Competência: {proc['competencia']}",
            f"Regime: {proc['regime']}",
            f"Status: {cls.status_emoji(proc['porcentagem'])} {proc['status']}",
            f"Progresso: {cls.barra_progresso(proc['porcentagem'])} {proc['porcentagem']:.1f}%",
            "",
            "⏱️ TEMPO",
            cls.SEPARADOR,
            f"Início: {proc['data_inicio'][:10] if proc['data_inicio'] else 'N/A'}",
            f"Dias Corridos: {proc['dias_corridos']} dias",
            ""
        ]
        
        # Passos
        if dados.get('passos'):
            linhas.extend([
                "📌 SITUAÇÃO ATUAL",
                cls.SEPARADOR
            ])
            
            for passo in dados['passos'][:5]:
                status_icon = "✅" if passo['concluido'] else "🔴"
                linhas.append(f"{status_icon} {passo['nome'][:35]}")
            
            if len(dados['passos']) > 5:
                linhas.append(f"... e mais {len(dados['passos']) - 5} passos")
            linhas.append("")
        
        # Desdobramentos pendentes
        desd_pendentes = [d for d in dados.get('desdobramentos', []) if not d['respondido']]
        if desd_pendentes:
            linhas.extend([
                "🚧 BLOQUEIOS",
                cls.SEPARADOR,
                "⚠️ Aguardando resposta:"
            ])
            
            for desd in desd_pendentes[:3]:
                linhas.append(f"   {desd['pergunta'][:35]}")
            
            if len(desd_pendentes) > 3:
                linhas.append(f"   ... e mais {len(desd_pendentes) - 3}")
            linhas.append("")
        
        linhas.extend([
            cls.SEPARADOR,
            "✅ Ação Recomendada:",
            "Contatar empresa para confirmar",
            "informações pendentes",
            cls.SEPARADOR,
            "",
            "Digite outro número ou 0 para menu"
        ])
        
        return "\n".join(linhas)
    
    # ============ MENSAGENS DE ERRO ============
    
    @classmethod
    def erro_nao_autorizado(cls) -> str:
        """Mensagem de erro - não autorizado"""
        return """
🚫 ACESSO NÃO AUTORIZADO

Você não tem permissão para usar
este sistema.

Entre em contato com o administrador.
"""
    
    @classmethod
    def erro_comando_invalido(cls, comando: str) -> str:
        """Mensagem de erro - comando inválido"""
        return f"""
❌ COMANDO INVÁLIDO

O comando "{comando}" não foi reconhecido.

Digite "0" ou "menu" para ver os
comandos disponíveis.
"""
    
    @classmethod
    def ajuda(cls) -> str:
        """Mensagem de ajuda"""
        return """
{cls.box_title("💡 AJUDA - COMANDOS")}

📝 COMO USAR:
{cls.SEPARADOR}
• Digite o NÚMERO do comando
  Ex: "1" para Resumo Geral

• Ou digite PALAVRA-CHAVE
  Ex: "resumo" ou "empresas"

• Digite "0" ou "menu" para
  voltar ao menu principal

🔎 BUSCAR EMPRESA:
{cls.SEPARADOR}
• Digite "20" e depois o nome
• Ou digite "21" e depois o CNPJ
• Ou digite direto o nome/CNPJ

💬 EXEMPLOS:
{cls.SEPARADOR}
1️⃣ Digite "1" → Resumo Geral
2️⃣ Digite "4" → Sem Faturamento
3️⃣ Digite "MOUSSA" → Busca empresa
4️⃣ Digite "0" → Menu Principal

{cls.SEPARADOR}

Digite "0" para voltar ao menu
"""


# ============ TESTE ============

if __name__ == "__main__":
    print("🎨 Testando Formatador WhatsApp...\n")
    
    # Teste: Menu Principal
    print(WhatsAppFormatter.menu_principal())
    
    print("\n" + "="*50)
    print("✅ Formatador OK!")
