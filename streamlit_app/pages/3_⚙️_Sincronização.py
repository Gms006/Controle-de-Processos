"""
⚙️ SINCRONIZAÇÃO - Atualização de Dados
Gerenciamento de sincronização com API Acessórias
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from utils import DatabaseManager, SyncManager, format_datetime
from components import alert_box, empty_state


# ============ CONFIGURAÇÃO ============
st.set_page_config(
    page_title="Sincronização | Gestão Acessórias",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Sincronização de Dados")
st.markdown("**Atualize os dados do sistema com a API Acessórias**")
st.markdown("---")


# ============ CARREGAR CONFIGURAÇÕES ============
@st.cache_resource
def get_db():
    return DatabaseManager()

db = get_db()


# ============ VERIFICAR SECRETS ============
try:
    api_token = st.secrets["api"]["ACESSORIAS_API_TOKEN"]
    api_url = st.secrets["api"]["ACESSORIAS_API_URL"]
    secrets_ok = True
except:
    secrets_ok = False
    api_token = None
    api_url = "https://api.acessorias.com"


# ============ STATUS DA ÚLTIMA SINCRONIZAÇÃO ============
st.markdown("## 📊 Status Atual")

ultima_sync = db.get_ultima_sincronizacao()

if ultima_sync:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🕐 Última Atualização",
            format_datetime(ultima_sync['concluida_em'])
        )
    
    with col2:
        st.metric(
            "📋 Processos Sincronizados",
            int(ultima_sync['total_processos'])
        )
    
    with col3:
        st.metric(
            "🆕 Novos",
            int(ultima_sync['processos_novos'])
        )
    
    with col4:
        st.metric(
            "🔄 Atualizados",
            int(ultima_sync['processos_atualizados'])
        )
    
    # Tempo desde última sync
    try:
        ultima_data = datetime.fromisoformat(ultima_sync['concluida_em'])
        tempo_desde = datetime.now() - ultima_data
        horas = int(tempo_desde.total_seconds() / 3600)
        
        if horas < 1:
            alert_box("✅ Dados atualizados recentemente!", "success")
        elif horas < 6:
            alert_box(f"ℹ️ Última atualização há {horas} hora(s)", "info")
        else:
            alert_box(f"⚠️ Última atualização há {horas} hora(s). Considere sincronizar novamente.", "warning")
    except:
        pass

else:
    alert_box("⚠️ Nenhuma sincronização realizada ainda. Execute a primeira sincronização abaixo.", "warning")

st.markdown("---")


# ============ SINCRONIZAÇÃO MANUAL ============
st.markdown("## 🔄 Sincronização Manual")

if not secrets_ok:
    st.error("❌ **Configuração incompleta!**")
    st.markdown("""
    Para usar a sincronização, configure o arquivo `.streamlit/secrets.toml`:
    
    ```toml
    [api]
    ACESSORIAS_API_TOKEN = "seu_token_aqui"
    ACESSORIAS_API_URL = "https://api.acessorias.com"
    ```
    
    **No Streamlit Cloud:**
    1. Acesse as configurações do app
    2. Vá em "Secrets"
    3. Cole a configuração acima com seu token real
    """)
    st.stop()

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### 📝 Como funciona:
    
    1. **Conecta** com a API Acessórias
    2. **Busca** todos os processos (Simples Nacional, Lucro Presumido, Lucro Real)
    3. **Atualiza** apenas processos modificados
    4. **Salva** no banco de dados local
    
    **Tempo estimado:** 1-3 minutos (depende da quantidade de dados)
    """)

with col2:
    competencia_sync = st.text_input(
        "📅 Competência (opcional)",
        placeholder="2025-11",
        help="Deixe em branco para sincronizar todas"
    )
    
    st.markdown("")
    st.markdown("")
    
    if st.button("🚀 Iniciar Sincronização", type="primary", use_container_width=True):
        with st.spinner("🔄 Sincronizando dados..."):
            try:
                sync_manager = SyncManager(
                    api_token=api_token,
                    api_url=api_url
                )
                
                # Criar progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("📡 Conectando à API...")
                progress_bar.progress(10)
                
                # Executar sincronização
                status_text.text("📋 Buscando processos...")
                progress_bar.progress(30)
                
                resultado = sync_manager.sync_processos(
                    competencia=competencia_sync if competencia_sync else None
                )
                
                progress_bar.progress(100)
                status_text.text("✅ Sincronização concluída!")
                
                st.success(f"""
                ✅ **Sincronização concluída com sucesso!**
                
                - 📊 **Total:** {resultado['total_processos']} processos
                - 🆕 **Novos:** {resultado['processos_novos']}
                - 🔄 **Atualizados:** {resultado['processos_atualizados']}
                - ⏱️ **Tempo:** {resultado['tempo_execucao']}s
                """)
                
                # Limpar cache para forçar reload dos dados
                st.cache_data.clear()
                
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Erro na sincronização: {str(e)}")
                st.markdown("""
                **Possíveis causas:**
                - Token da API inválido ou expirado
                - Problemas de conexão com a internet
                - API Acessórias fora do ar
                
                Verifique suas credenciais e tente novamente.
                """)

st.markdown("---")


# ============ HISTÓRICO DE SINCRONIZAÇÕES ============
st.markdown("## 📜 Histórico de Sincronizações")

historico_df = db.get_historico_sincronizacoes(limit=20)

if len(historico_df) > 0:
    # Preparar dados
    df_display = historico_df.copy()
    
    # Formatar colunas
    df_display['iniciada_em'] = df_display['iniciada_em'].apply(format_datetime)
    df_display['concluida_em'] = df_display['concluida_em'].apply(format_datetime)
    
    # Adicionar indicador de status
    df_display['status_icon'] = df_display['status'].apply(
        lambda x: '✅' if x == 'CONCLUIDA' else '❌' if x == 'ERRO' else '⏳'
    )
    
    # Renomear colunas
    colunas_renomeadas = {
        'tipo': 'Tipo',
        'competencia': 'Competência',
        'total_processos': 'Total',
        'processos_novos': 'Novos',
        'processos_atualizados': 'Atualizados',
        'status': 'Status',
        'status_icon': '',
        'tempo_execucao': 'Tempo (s)',
        'iniciada_em': 'Início',
        'concluida_em': 'Conclusão'
    }
    
    df_display = df_display.rename(columns=colunas_renomeadas)
    
    # Selecionar colunas
    colunas_exibir = [
        '', 'Início', 'Tipo', 'Competência', 'Total', 
        'Novos', 'Atualizados', 'Tempo (s)', 'Status'
    ]
    
    st.dataframe(
        df_display[colunas_exibir],
        use_container_width=True,
        hide_index=True,
        height=400
    )
    
    st.info(f"ℹ️ Mostrando as últimas 20 sincronizações de {len(historico_df)} total")

else:
    empty_state("Nenhuma sincronização encontrada no histórico")


# ============ INFORMAÇÕES ADICIONAIS ============
st.markdown("---")
st.markdown("## ℹ️ Informações Importantes")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🔐 Segurança
    - Token da API nunca é exibido
    - Dados armazenados localmente em SQLite
    - Sem envio de dados para terceiros
    
    ### ⚡ Performance
    - Sincronização incremental (apenas mudanças)
    - Cache inteligente de 5 minutos
    - Índices otimizados no banco
    """)

with col2:
    st.markdown("""
    ### 📊 Dados Sincronizados
    - ✅ Simples Nacional
    - ✅ Lucro Presumido (Serviços e Comércio)
    - ✅ Lucro Real (Serviços e Comércio)
    - ✅ Passos e desdobramentos
    
    ### 🔄 Frequência Recomendada
    - **Manual:** Quando necessário
    - **Automática:** A cada 6 horas (via GitHub Actions)
    """)


# ============ FOOTER ============
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>🔄 <b>Sincronização com API Acessórias</b></p>
        <p>Dados sempre atualizados e confiáveis</p>
    </div>
    """,
    unsafe_allow_html=True
)
