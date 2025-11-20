"""
Script Profissional para Popular Banco de Dados
- Lê sempre os arquivos Excel mais recentes
- Atualiza dados existentes automaticamente
- Evita duplicações
- Log detalhado de operações
"""

import sys
from pathlib import Path
import pandas as pd
from datetime import datetime
from collections import defaultdict

# Adicionar backend ao path
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from app.database import SessionLocal, engine, Base
from app.models import Empresa, Processo, Passo, Desdobramento, Sincronizacao

# Criar todas as tabelas
Base.metadata.create_all(bind=engine)

class PopuladorBanco:
    def __init__(self):
        self.db = SessionLocal()
        self.planilhas_dir = Path(__file__).parent.parent / 'output' / 'planilhas'
        self.stats = {
            'empresas_novas': 0,
            'empresas_atualizadas': 0,
            'processos_novos': 0,
            'processos_atualizados': 0,
            'passos_total': 0,
            'desdobramentos_total': 0
        }
        
    def obter_arquivos_mais_recentes(self) -> dict:
        """
        Busca o arquivo Excel mais recente para cada regime
        """
        arquivos = list(self.planilhas_dir.glob('*.xlsx'))
        
        if not arquivos:
            print("❌ Nenhum arquivo Excel encontrado!")
            return {}
        
        print(f"\n📁 Total de arquivos encontrados: {len(arquivos)}")
        
        # Agrupar por regime (prefixo do nome)
        arquivos_por_regime = defaultdict(list)
        
        for arquivo in arquivos:
            # Extrair regime do nome do arquivo
            nome = arquivo.stem
            regime = nome.split('_')[0]  # Primeira parte antes do _
            arquivos_por_regime[regime].append(arquivo)
        
        # Pegar o mais recente de cada regime
        arquivos_recentes = {}
        
        for regime, lista_arquivos in arquivos_por_regime.items():
            # Ordenar por data de modificação (mais recente primeiro)
            mais_recente = max(lista_arquivos, key=lambda f: f.stat().st_mtime)
            arquivos_recentes[regime] = mais_recente
            
            data_mod = datetime.fromtimestamp(mais_recente.stat().st_mtime)
            print(f"   ✅ {regime}: {mais_recente.name}")
            print(f"      Modificado em: {data_mod.strftime('%d/%m/%Y %H:%M:%S')}")
        
        return arquivos_recentes
    
    def processar_arquivo(self, arquivo: Path, regime: str):
        """
        Processa um arquivo Excel e popula o banco
        """
        print(f"\n📊 Processando {regime}...")
        print(f"   Arquivo: {arquivo.name}")
        
        try:
            # Ler Excel
            xl = pd.ExcelFile(arquivo)
            
            # Determinar qual aba ler
            aba_processos = None
            if 'PROCESSOS_GERAL' in xl.sheet_names:
                aba_processos = 'PROCESSOS_GERAL'
                aba_passos = 'PROCESSOS_PASSOS'
                aba_desdobramentos = 'PROCESSOS_DESDOBRAMENTOS'
            elif 'PROCESSOS' in xl.sheet_names:
                aba_processos = 'PROCESSOS'
                aba_passos = 'PASSOS'
                aba_desdobramentos = 'DESDOBRAMENTOS'
            else:
                print(f"   ⚠️  Estrutura de abas desconhecida: {xl.sheet_names}")
                return
            
            # Ler dados
            df_processos = pd.read_excel(arquivo, sheet_name=aba_processos)
            df_passos = pd.read_excel(arquivo, sheet_name=aba_passos)
            df_desdobramentos = pd.read_excel(arquivo, sheet_name=aba_desdobramentos)
            
            print(f"   📋 {len(df_processos)} processos, {len(df_passos)} passos, {len(df_desdobramentos)} desdobramentos")
            
            # Processar cada processo
            processos_inseridos = 0
            processos_atualizados = 0
            
            for _, row in df_processos.iterrows():
                proc_id = int(row['PROC_ID'])
                
                # Verificar se processo já existe
                processo_existente = self.db.query(Processo).filter(
                    Processo.proc_id == proc_id
                ).first()
                
                # Obter ou criar empresa
                empresa = self._obter_ou_criar_empresa(row, regime)
                
                if processo_existente:
                    # ATUALIZAR processo existente
                    processo = processo_existente
                    processo.nome = str(row['PROCESSO'])
                    processo.status = str(row.get('STATUS', 'N/A'))
                    processo.porcentagem_conclusao = float(row.get('PORCENTAGEM', 0))
                    processo.dias_corridos = int(row.get('DIAS_CORRIDOS', 0))
                    processo.regime_tributario = regime
                    processo.competencia = "10/2025"
                    
                    # Deletar passos e desdobramentos antigos
                    self.db.query(Passo).filter(Passo.processo_id == processo.id).delete()
                    self.db.query(Desdobramento).filter(Desdobramento.processo_id == processo.id).delete()
                    
                    processos_atualizados += 1
                else:
                    # CRIAR novo processo
                    processo = Processo(
                        proc_id=proc_id,
                        empresa_id=empresa.id,
                        nome=str(row['PROCESSO']),
                        competencia="10/2025",
                        status=str(row.get('STATUS', 'N/A')),
                        porcentagem_conclusao=float(row.get('PORCENTAGEM', 0)),
                        dias_corridos=int(row.get('DIAS_CORRIDOS', 0)),
                        regime_tributario=regime
                    )
                    self.db.add(processo)
                    processos_inseridos += 1
                
                self.db.flush()  # Para obter processo.id
                
                # Adicionar passos
                passos_processo = df_passos[df_passos['PROC_ID'] == proc_id]
                for idx, passo_row in passos_processo.iterrows():
                    passo = Passo(
                        processo_id=processo.id,
                        passo_id=int(passo_row.get('PASSO_ID', idx)),
                        ordem=int(passo_row.get('ORDEM', idx)),
                        nome=str(passo_row['PASSO']),
                        descricao=str(passo_row.get('DESCRICAO', '')),
                        concluido=bool(passo_row.get('CONCLUIDO', False))
                    )
                    self.db.add(passo)
                    self.stats['passos_total'] += 1
                
                # Adicionar desdobramentos
                desdobr_processo = df_desdobramentos[df_desdobramentos['PROC_ID'] == proc_id]
                for idx, desdobr_row in desdobr_processo.iterrows():
                    desdobr = Desdobramento(
                        processo_id=processo.id,
                        desdobramento_id=int(desdobr_row.get('DESDOBR_ID', idx)),
                        pergunta=str(desdobr_row.get('PERGUNTA', '')),
                        resposta=str(desdobr_row.get('RESPOSTA', '')) if pd.notna(desdobr_row.get('RESPOSTA')) else None,
                        tipo=str(desdobr_row.get('TIPO', 'BINARIO')),
                        ordem=int(desdobr_row.get('ORDEM', idx)),
                        respondido=bool(desdobr_row.get('RESPONDIDO', False))
                    )
                    self.db.add(desdobr)
                    self.stats['desdobramentos_total'] += 1
            
            self.db.commit()
            
            print(f"   ✅ Inseridos: {processos_inseridos}, Atualizados: {processos_atualizados}")
            
            self.stats['processos_novos'] += processos_inseridos
            self.stats['processos_atualizados'] += processos_atualizados
            
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            self.db.rollback()
            raise
    
    def _obter_ou_criar_empresa(self, row, regime: str) -> Empresa:
        """
        Busca empresa existente ou cria nova
        """
        # Usar PROC_ID como código único (mais confiável)
        empresa_nome = str(row['EMPRESA'])
        codigo_empresa = f"{regime}_{empresa_nome[:20]}"  # Código único por regime
        
        empresa = self.db.query(Empresa).filter(
            Empresa.codigo == codigo_empresa
        ).first()
        
        if not empresa:
            empresa = Empresa(
                codigo=codigo_empresa,
                nome=empresa_nome,
                regime_tributario=regime,
                ativa=True
            )
            self.db.add(empresa)
            self.db.flush()
            self.stats['empresas_novas'] += 1
        else:
            # Atualizar nome se mudou
            if empresa.nome != empresa_nome:
                empresa.nome = empresa_nome
                self.stats['empresas_atualizadas'] += 1
        
        return empresa
    
    def registrar_sincronizacao(self):
        """
        Registra log da sincronização
        """
        sync_log = Sincronizacao(
            tipo="FULL",
            competencia="10/2025",
            total_processos=self.stats['processos_novos'] + self.stats['processos_atualizados'],
            processos_novos=self.stats['processos_novos'],
            processos_atualizados=self.stats['processos_atualizados'],
            status="CONCLUIDA",
            tempo_execucao=0,
            concluida_em=datetime.now()
        )
        self.db.add(sync_log)
        self.db.commit()
    
    def executar(self):
        """
        Executa o processo completo de população
        """
        inicio = datetime.now()
        
        print("\n" + "=" * 70)
        print(" 🚀 POPULAÇÃO DO BANCO DE DADOS - MODO PROFISSIONAL")
        print("=" * 70)
        print(" Estratégia: Sempre os arquivos mais recentes")
        print(" Comportamento: Atualiza dados existentes")
        print("=" * 70)
        
        try:
            # 1. Obter arquivos mais recentes
            arquivos = self.obter_arquivos_mais_recentes()
            
            if not arquivos:
                return
            
            # 2. Processar cada arquivo
            for regime, arquivo in arquivos.items():
                self.processar_arquivo(arquivo, regime)
            
            # 3. Registrar sincronização
            self.registrar_sincronizacao()
            
            # 4. Mostrar resumo
            tempo_total = (datetime.now() - inicio).seconds
            
            print("\n" + "=" * 70)
            print(" ✅ POPULAÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 70)
            print(f" ⏱️  Tempo total: {tempo_total}s")
            print(f"\n📊 ESTATÍSTICAS:")
            print(f"   • Empresas novas: {self.stats['empresas_novas']}")
            print(f"   • Empresas atualizadas: {self.stats['empresas_atualizadas']}")
            print(f"   • Processos novos: {self.stats['processos_novos']}")
            print(f"   • Processos atualizados: {self.stats['processos_atualizados']}")
            print(f"   • Total de passos: {self.stats['passos_total']}")
            print(f"   • Total de desdobramentos: {self.stats['desdobramentos_total']}")
            
            # 5. Verificar totais no banco
            total_empresas = self.db.query(Empresa).count()
            total_processos = self.db.query(Processo).count()
            total_passos = self.db.query(Passo).count()
            total_desdobr = self.db.query(Desdobramento).count()
            
            print(f"\n💾 TOTAIS NO BANCO DE DADOS:")
            print(f"   • Empresas: {total_empresas}")
            print(f"   • Processos: {total_processos}")
            print(f"   • Passos: {total_passos}")
            print(f"   • Desdobramentos: {total_desdobr}")
            print("=" * 70 + "\n")
            
        except Exception as e:
            print(f"\n❌ ERRO FATAL: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.db.close()

if __name__ == "__main__":
    populador = PopuladorBanco()
    populador.executar()
