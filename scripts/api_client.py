"""
API Client - Acessórias
Gerencia conexão e comunicação com a API Acessórias
"""

import requests
import time
import json
import logging
from typing import Optional, Dict, List
from datetime import datetime, timedelta


class AcessoriasAPI:
    """Cliente para interação com a API Acessórias"""
    
    def __init__(self, api_token: str, base_url: str = "https://api.acessorias.com"):
        self.api_token = api_token
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_token}'
        })
        
        # Rate limiting (90 req/min com margem de segurança)
        self.max_requests_per_minute = 90
        self.request_times = []
        
        logging.info("Cliente API Acessórias inicializado")
    
    def _check_rate_limit(self):
        """Verifica e respeita o rate limit da API (90 req/min)"""
        now = datetime.now()
        one_minute_ago = now - timedelta(minutes=1)
        
        # Remove requisições antigas (mais de 1 minuto)
        self.request_times = [t for t in self.request_times if t > one_minute_ago]
        
        # Se atingiu o limite, aguarda
        if len(self.request_times) >= self.max_requests_per_minute:
            sleep_time = 60 - (now - self.request_times[0]).total_seconds()
            if sleep_time > 0:
                logging.warning(f"Rate limit atingido. Aguardando {sleep_time:.2f} segundos...")
                time.sleep(sleep_time)
                self.request_times = []
        
        # Registra o tempo desta requisição
        self.request_times.append(now)
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict]:
        """Faz requisição HTTP com tratamento de erros e rate limit"""
        self._check_rate_limit()
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(method, url, timeout=30, **kwargs)
            
            # Tratamento de erros HTTP
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 204:
                logging.info(f"Nenhum conteúdo retornado para {endpoint}")
                return None
            elif response.status_code == 401:
                logging.error("Erro 401: Token inválido ou expirado")
                raise Exception("Autenticação falhou. Verifique seu API_TOKEN")
            elif response.status_code == 404:
                logging.error(f"Erro 404: Endpoint não encontrado - {endpoint}")
                return None
            elif response.status_code == 429:
                logging.warning("Erro 429: Rate limit excedido")
                time.sleep(60)
                return self._make_request(method, endpoint, **kwargs)
            else:
                logging.error(f"Erro {response.status_code}: {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            logging.error(f"Timeout na requisição para {endpoint}")
            return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro na requisição: {e}")
            return None
        except json.JSONDecodeError:
            logging.error("Erro ao decodificar JSON da resposta")
            return None
    
    def get_processes(self, proc_id: str = "ListAll", **params) -> Optional[List[Dict]]:
        """
        Busca processos da API
        
        Args:
            proc_id: ID do processo ou "ListAll" para todos
            **params: Query parameters (ProcStatus, ProcNome, Pagina, DtLastDH, etc.)
        
        Returns:
            Lista de processos ou None em caso de erro
        """
        endpoint = f"/processes/{proc_id}"
        
        # Adiciona query parameters
        if params:
            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            endpoint += f"/?{query_string}"
        
        logging.info(f"Buscando processos: {endpoint}")
        result = self._make_request("GET", endpoint)
        
        # API retorna lista ou dict, normalizar para lista
        if result is not None:
            if isinstance(result, dict):
                return [result]
            return result
        return None
    
    def get_all_processes_paginated(self, proc_status: str = None, proc_nome: str = None, with_details: bool = False) -> List[Dict]:
        """
        Busca TODOS os processos paginados
        
        Args:
            proc_status: Filtro de status (A, C, S, D, P, W, X)
            proc_nome: Filtro por nome do processo
            with_details: Se True, busca detalhes de cada processo (inclui ProcPassos)
        
        Returns:
            Lista completa de todos os processos
        """
        all_processes = []
        page = 1
        
        while True:
            params = {"Pagina": page}
            
            if proc_status:
                params["ProcStatus"] = proc_status
            if proc_nome:
                params["ProcNome"] = proc_nome
            
            logging.info(f"Buscando página {page}...")
            processes = self.get_processes("ListAll", **params)
            
            # Se retornou vazio, terminou a paginação
            if not processes or len(processes) == 0:
                logging.info(f"Paginação finalizada. Total de {len(all_processes)} processos")
                break
            
            all_processes.extend(processes)
            logging.info(f"Página {page}: {len(processes)} processos | Total acumulado: {len(all_processes)}")
            page += 1
            
            # Pequeno delay entre páginas para ser gentil com a API
            time.sleep(0.5)
        
        # Se quiser detalhes, buscar cada processo individualmente
        if with_details and all_processes:
            logging.info(f"\n🔍 Buscando detalhes completos de {len(all_processes)} processos...")
            logging.info("(Isso pode demorar um pouco...)")
            
            detailed_processes = []
            for i, proc in enumerate(all_processes, 1):
                proc_id = proc.get('ProcID')
                if proc_id:
                    logging.info(f"  [{i}/{len(all_processes)}] Buscando detalhes do processo {proc_id}...")
                    detailed = self.get_processes(proc_id)
                    if detailed and len(detailed) > 0:
                        detailed_processes.append(detailed[0])
                    else:
                        # Se falhar, mantém o processo sem detalhes
                        detailed_processes.append(proc)
                    
                    # Delay para respeitar rate limit
                    if i % 10 == 0:
                        logging.info(f"  Aguardando 1 segundo (rate limit)...")
                        time.sleep(1)
            
            logging.info(f"✓ Detalhes completos obtidos para {len(detailed_processes)} processos")
            return detailed_processes
        
        return all_processes
    
    def get_companies(self, identificador: str = "ListAll", **params) -> Optional[Dict]:
        """Busca empresas da API"""
        endpoint = f"/companies/{identificador}"
        
        if params:
            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            endpoint += f"/?{query_string}"
        
        logging.info(f"Buscando empresas: {endpoint}")
        return self._make_request("GET", endpoint)
    
    def get_deliveries(self, identificador: str, dt_initial: str, dt_final: str, **params) -> Optional[List[Dict]]:
        """Busca entregas da API"""
        endpoint = f"/deliveries/{identificador}/?DtInitial={dt_initial}&DtFinal={dt_final}"
        
        if params:
            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            endpoint += f"&{query_string}"
        
        logging.info(f"Buscando entregas: {endpoint}")
        return self._make_request("GET", endpoint)
