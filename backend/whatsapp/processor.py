"""
Processador de Comandos WhatsApp
Interpreta comandos e roteia para análises corretas
"""

from typing import Dict, Optional, Tuple
from .analytics import GestorAnalytics
from .formatador import WhatsAppFormatter


class CommandProcessor:
    """
    Processador de comandos recebidos via WhatsApp
    Identifica o comando e gera a resposta apropriada
    """
    
    # Mapeamento de comandos
    COMANDOS = {
        # Resumos Executivos
        '1': 'resumo_geral',
        'resumo geral': 'resumo_geral',
        'resumo': 'resumo_geral',
        'kpis': 'resumo_geral',
        
        '2': 'resumo_regime',
        'resumo regime': 'resumo_regime',
        'por regime': 'resumo_regime',
        'regimes': 'resumo_regime',
        
        '3': 'resumo_empresa',
        'resumo empresa': 'resumo_empresa',
        'empresas': 'resumo_empresa',
        
        # Análises Específicas
        '4': 'sem_faturamento',
        'sem faturamento': 'sem_faturamento',
        'faturamento': 'sem_faturamento',
        
        '5': 'com_tributos',
        'tributos': 'com_tributos',
        'com tributos': 'com_tributos',
        'apurados': 'com_tributos',
        
        '6': 'declaracoes_pendentes',
        'declarações': 'declaracoes_pendentes',
        'pendentes': 'declaracoes_pendentes',
        'obrigações': 'declaracoes_pendentes',
        
        '7': 'declaracoes_dispensadas',
        'dispensadas': 'declaracoes_dispensadas',
        
        # Desempenho
        '8': 'tempo_finalizacao',
        'tempo': 'tempo_finalizacao',
        'finalização': 'tempo_finalizacao',
        'finalizacao': 'tempo_finalizacao',
        
        '9': 'processos_atrasados',
        'atrasados': 'processos_atrasados',
        'críticos': 'processos_atrasados',
        'criticos': 'processos_atrasados',
        
        '10': 'top_rapidas',
        'rápidas': 'top_rapidas',
        'rapidas': 'top_rapidas',
        
        '11': 'top_lentas',
        'lentas': 'top_lentas',
        
        # Alertas
        '12': 'empresas_paradas',
        'paradas': 'empresas_paradas',
        'bloqueadas': 'empresas_paradas',
        
        '13': 'gargalos',
        'gargalo': 'gargalos',
        
        '14': 'desdobramentos_pendentes',
        'desdobramentos': 'desdobramentos_pendentes',
        
        '15': 'obrigacoes_pendentes',
        
        # Busca
        '20': 'buscar_empresa_nome',
        '21': 'buscar_empresa_cnpj',
        '22': 'filtrar_status',
        
        # Menu e ajuda
        '0': 'menu',
        'menu': 'menu',
        'inicio': 'menu',
        'início': 'menu',
        
        '23': 'ajuda',
        'ajuda': 'ajuda',
        'help': 'ajuda',
        '?': 'ajuda',
        
        '24': 'sobre',
        'sobre': 'sobre',
    }
    
    def __init__(self, competencia: str = '10/2025'):
        self.competencia = competencia
        self.analytics = GestorAnalytics()
        self.formatter = WhatsAppFormatter()
        
        # Estado da conversação (para comandos em múltiplas etapas)
        self.user_states = {}
    
    def processar(self, mensagem: str, telefone: str) -> str:
        """
        Processa comando e retorna resposta formatada
        
        Args:
            mensagem: Texto da mensagem recebida
            telefone: Número do telefone do remetente
            
        Returns:
            Resposta formatada para enviar via WhatsApp
        """
        # Normalizar mensagem
        cmd = mensagem.strip().lower()
        
        # Verificar se há estado pendente (comando em múltiplas etapas)
        if telefone in self.user_states:
            return self._processar_com_estado(cmd, telefone)
        
        # Identificar comando
        comando = self._identificar_comando(cmd)
        
        if not comando:
            # Tentar busca direta por nome de empresa
            if len(cmd) > 3:
                return self._executar_buscar_empresa(cmd)
            return self.formatter.erro_comando_invalido(cmd)
        
        # Executar comando
        return self._executar_comando(comando, cmd, telefone)
    
    def _identificar_comando(self, cmd: str) -> Optional[str]:
        """Identifica comando na mensagem"""
        # Busca exata
        if cmd in self.COMANDOS:
            return self.COMANDOS[cmd]
        
        # Busca parcial (palavras-chave)
        for chave, comando in self.COMANDOS.items():
            if chave in cmd or cmd in chave:
                return comando
        
        return None
    
    def _executar_comando(self, comando: str, mensagem: str, telefone: str) -> str:
        """Executa comando identificado"""
        try:
            # Menu e ajuda
            if comando == 'menu':
                return self.formatter.menu_principal()
            
            if comando == 'ajuda':
                return self.formatter.ajuda()
            
            if comando == 'sobre':
                return self._executar_sobre()
            
            # Resumos
            if comando == 'resumo_geral':
                return self._executar_resumo_geral()
            
            if comando == 'resumo_regime':
                return self._executar_resumo_regime()
            
            if comando == 'resumo_empresa':
                return self._executar_resumo_empresa()
            
            # Análises
            if comando == 'sem_faturamento':
                return self._executar_sem_faturamento()
            
            if comando == 'com_tributos':
                return self._executar_com_tributos()
            
            if comando == 'declaracoes_pendentes':
                return self._executar_declaracoes_pendentes()
            
            # Desempenho
            if comando == 'tempo_finalizacao':
                return self._executar_tempo_finalizacao()
            
            if comando == 'top_rapidas':
                return self._executar_top_rapidas()
            
            if comando == 'top_lentas':
                return self._executar_top_lentas()
            
            # Alertas
            if comando == 'empresas_paradas':
                return self._executar_empresas_paradas()
            
            if comando == 'gargalos':
                return self._executar_gargalos()
            
            if comando == 'desdobramentos_pendentes':
                return self._executar_desdobramentos_pendentes()
            
            # Busca
            if comando == 'buscar_empresa_nome':
                self.user_states[telefone] = 'aguardando_nome_empresa'
                return "🔎 Digite o nome da empresa:"
            
            if comando == 'buscar_empresa_cnpj':
                self.user_states[telefone] = 'aguardando_cnpj_empresa'
                return "🔎 Digite o CNPJ da empresa:"
            
            return self.formatter.erro_comando_invalido(mensagem)
            
        except Exception as e:
            return f"❌ Erro ao processar comando:\n{str(e)}\n\nDigite 0 para voltar ao menu"
    
    def _processar_com_estado(self, mensagem: str, telefone: str) -> str:
        """Processa comando com estado (múltiplas etapas)"""
        estado = self.user_states.get(telefone)
        
        # Limpar estado
        del self.user_states[telefone]
        
        if estado == 'aguardando_nome_empresa':
            return self._executar_buscar_empresa(mensagem)
        
        if estado == 'aguardando_cnpj_empresa':
            return self._executar_buscar_empresa(mensagem)
        
        return self.formatter.erro_comando_invalido(mensagem)
    
    # ============ EXECUTORES DE COMANDOS ============
    
    def _executar_resumo_geral(self) -> str:
        """Executa comando: Resumo Geral"""
        dados = self.analytics.get_resumo_geral(self.competencia)
        return self.formatter.resumo_geral(dados)
    
    def _executar_resumo_regime(self) -> str:
        """Executa comando: Resumo por Regime"""
        dados = self.analytics.get_resumo_por_regime(self.competencia)
        return self.formatter.resumo_por_regime(dados)
    
    def _executar_resumo_empresa(self) -> str:
        """Executa comando: Resumo por Empresa"""
        # Por enquanto redireciona para busca
        return "🔎 Digite o nome ou CNPJ da empresa para ver o resumo:"
    
    def _executar_sem_faturamento(self) -> str:
        """Executa comando: Empresas sem Faturamento"""
        dados = self.analytics.get_empresas_sem_faturamento(self.competencia)
        return self.formatter.empresas_sem_faturamento(dados)
    
    def _executar_com_tributos(self) -> str:
        """Executa comando: Empresas com Tributos"""
        dados = self.analytics.get_empresas_com_tributos(self.competencia)
        return self.formatter.empresas_com_tributos(dados)
    
    def _executar_declaracoes_pendentes(self) -> str:
        """Executa comando: Declarações Pendentes"""
        dados = self.analytics.get_declaracoes_pendentes(self.competencia)
        return self.formatter.declaracoes_pendentes(dados)
    
    def _executar_tempo_finalizacao(self) -> str:
        """Executa comando: Tempo de Finalização"""
        dados = self.analytics.get_tempo_finalizacao(self.competencia)
        return self.formatter.tempo_finalizacao(dados)
    
    def _executar_top_rapidas(self) -> str:
        """Executa comando: Top 10 Mais Rápidas"""
        dados = self.analytics.get_tempo_finalizacao(self.competencia)
        
        if dados.get('total_concluidos', 0) == 0:
            return "⚠️ Nenhum processo concluído ainda.\n\nDigite outro número ou 0 para menu"
        
        # Formatar apenas top rápidas
        linhas = [
            "🏆 TOP 10 - EMPRESAS MAIS RÁPIDAS",
            self.formatter.SEPARADOR,
            ""
        ]
        
        for i, emp in enumerate(dados['top_rapidas'][:10], 1):
            linhas.extend([
                f"{i}. {emp['empresa'][:30]}",
                f"   Regime: {emp['regime']}",
                f"   ⏱️ {emp['dias']} dias | ✅ {emp['porcentagem']:.0f}%",
                ""
            ])
        
        linhas.extend([
            self.formatter.SEPARADOR,
            "",
            "Digite outro número ou 0 para menu"
        ])
        
        return "\n".join(linhas)
    
    def _executar_top_lentas(self) -> str:
        """Executa comando: Top 10 Mais Lentas"""
        dados = self.analytics.get_tempo_finalizacao(self.competencia)
        
        if dados.get('total_concluidos', 0) == 0:
            return "⚠️ Nenhum processo concluído ainda.\n\nDigite outro número ou 0 para menu"
        
        # Formatar apenas top lentas
        linhas = [
            "🐌 TOP 10 - EMPRESAS MAIS LENTAS",
            self.formatter.SEPARADOR,
            ""
        ]
        
        for i, emp in enumerate(dados['top_lentas'][:10], 1):
            linhas.extend([
                f"{i}. {emp['empresa'][:30]}",
                f"   Regime: {emp['regime']}",
                f"   ⏱️ {emp['dias']} dias | ✅ {emp['porcentagem']:.0f}%",
                f"   Gargalo: {emp['gargalo'][:35]}",
                ""
            ])
        
        linhas.extend([
            self.formatter.SEPARADOR,
            "",
            "Digite outro número ou 0 para menu"
        ])
        
        return "\n".join(linhas)
    
    def _executar_empresas_paradas(self) -> str:
        """Executa comando: Empresas Paradas"""
        dados = self.analytics.get_empresas_paradas(self.competencia)
        return self.formatter.empresas_paradas(dados)
    
    def _executar_gargalos(self) -> str:
        """Executa comando: Gargalos por Tipo de Passo"""
        dados = self.analytics.get_gargalos_por_passo(self.competencia)
        
        linhas = [
            "🚧 GARGALOS POR TIPO DE PASSO",
            self.formatter.SEPARADOR,
            f"Total de Passos Pendentes: {dados['total_passos_pendentes']}",
            "",
            "🔝 TOP 10 GARGALOS:",
            self.formatter.SEPARADOR
        ]
        
        for i, gargalo in enumerate(dados['top_10_gargalos'], 1):
            linhas.append(f"{i}. {gargalo['passo'][:35]}")
            linhas.append(f"   Quantidade: {gargalo['quantidade']} empresas")
            linhas.append("")
        
        linhas.extend([
            self.formatter.SEPARADOR,
            "",
            "Digite outro número ou 0 para menu"
        ])
        
        return "\n".join(linhas)
    
    def _executar_desdobramentos_pendentes(self) -> str:
        """Executa comando: Desdobramentos Não Respondidos"""
        dados = self.analytics.get_desdobramentos_pendentes(self.competencia)
        
        linhas = [
            "❓ DESDOBRAMENTOS NÃO RESPONDIDOS",
            self.formatter.SEPARADOR,
            f"Total Pendentes: {dados['total_pendentes']}",
            "",
            "🔝 TOP 20 PERGUNTAS:",
            self.formatter.SEPARADOR
        ]
        
        for i, pergunta in enumerate(dados['top_perguntas'], 1):
            linhas.append(f"{i}. {pergunta['pergunta'][:50]}")
            linhas.append(f"   Empresas: {pergunta['quantidade']}")
            linhas.append("")
        
        linhas.extend([
            self.formatter.SEPARADOR,
            "",
            "Digite outro número ou 0 para menu"
        ])
        
        return "\n".join(linhas)
    
    def _executar_buscar_empresa(self, termo: str) -> str:
        """Executa comando: Buscar Empresa"""
        resultados = self.analytics.buscar_empresa(termo)
        
        if not resultados:
            return f"❌ Nenhuma empresa encontrada com '{termo}'\n\nDigite outro termo ou 0 para menu"
        
        if len(resultados) == 1:
            # Buscar detalhes do processo mais recente
            empresa = resultados[0]
            if empresa['processos']:
                proc_id = empresa['processos'][0]['proc_id']
                detalhes = self.analytics.get_detalhes_processo(proc_id)
                if detalhes:
                    return self.formatter.detalhes_empresa(detalhes)
        
        # Múltiplos resultados - listar
        linhas = [
            f"🔎 RESULTADOS DA BUSCA: '{termo}'",
            self.formatter.SEPARADOR,
            f"Encontradas {len(resultados)} empresas:",
            ""
        ]
        
        for i, emp in enumerate(resultados[:10], 1):
            processo_atual = emp['processos'][0] if emp['processos'] else None
            
            linhas.extend([
                f"{i}. {emp['nome'][:35]}",
                f"   CNPJ: {emp['cnpj']}",
                f"   Regime: {emp['regime'] or 'N/A'}"
            ])
            
            if processo_atual:
                linhas.append(f"   Status: {processo_atual['status']} ({processo_atual['porcentagem']:.1f}%)")
            
            linhas.append("")
        
        if len(resultados) > 10:
            linhas.append(f"... e mais {len(resultados) - 10} empresas")
        
        linhas.extend([
            self.formatter.SEPARADOR,
            "Digite o número da empresa para",
            "ver detalhes, ou 0 para menu"
        ])
        
        return "\n".join(linhas)
    
    def _executar_sobre(self) -> str:
        """Executa comando: Sobre"""
        return f"""
{self.formatter.box_title("ℹ️ SOBRE O SISTEMA")}

📱 GESTOR DE PROCESSOS CONTÁBEIS
Versão: 1.0
Data: 18/11/2025

{self.formatter.SEPARADOR}
🎯 FUNCIONALIDADES:
{self.formatter.SEPARADOR}
• Análises em tempo real
• Métricas gerenciais completas
• Identificação de gargalos
• Alertas de processos parados
• Busca de empresas
• 100% gratuito (só recebe)

{self.formatter.SEPARADOR}
📊 DADOS ATUAIS:
{self.formatter.SEPARADOR}
• Competência: {self.competencia}
• Backend: FastAPI + SQLite
• Interface: WhatsApp Business API

{self.formatter.SEPARADOR}
✅ RECURSOS:
{self.formatter.SEPARADOR}
• 24 comandos disponíveis
• Formatação mobile-friendly
• Análises inteligentes
• Insights automáticos

{self.formatter.SEPARADOR}

Digite 0 para voltar ao menu
"""
    
    def fechar(self):
        """Fecha conexão com analytics"""
        if self.analytics:
            self.analytics.__exit__(None, None, None)


# ============ TESTE ============

if __name__ == "__main__":
    print("🤖 Testando Processador de Comandos...\n")
    
    processor = CommandProcessor()
    
    # Teste 1: Menu
    print("Teste 1: Menu")
    resposta = processor.processar("0", "+5511999999999")
    print(resposta[:200], "...\n")
    
    # Teste 2: Resumo Geral
    print("Teste 2: Resumo Geral")
    resposta = processor.processar("1", "+5511999999999")
    print(resposta[:200], "...\n")
    
    # Teste 3: Comando inválido
    print("Teste 3: Comando Inválido")
    resposta = processor.processar("xyz", "+5511999999999")
    print(resposta, "\n")
    
    processor.fechar()
    
    print("✅ Processador OK!")
