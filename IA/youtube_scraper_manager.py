# -*- coding: utf-8 -*-
"""
YouTube Scraper Manager - Sistema Completo Integrado
Executa scraping do YouTube em background com controle total
"""

import threading
import time
import queue
import logging
from datetime import datetime
from typing import Dict, List, Optional
import signal
import sys
import os
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper_manager.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class YouTubeVideoScraper:
    """Classe para extrair informações de vídeos do YouTube"""
    
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.driver = None
        
    def _setup_driver(self):
        """Configura o driver do Chrome com opções otimizadas"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=800,600')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        try:
            self.driver = webdriver.Chrome(
                ChromeDriverManager().install(), 
                options=options
            )
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            logger.info("Driver do Chrome inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar o driver: {e}")
            raise
    
    @contextmanager
    def _driver_context(self):
        """Context manager para gerenciar o ciclo de vida do driver"""
        try:
            self._setup_driver()
            yield self.driver
        finally:
            if self.driver:
                self.driver.quit()
                logger.info("Driver finalizado")
    
    def get_video_title(self, url):
        """
        Extrai o título de um vídeo do YouTube
        
        Args:
            url (str): URL do vídeo do YouTube
            
        Returns:
            str: Título do vídeo ou None se não encontrado
        """
        if not self._is_valid_youtube_url(url):
            logger.error("URL inválida ou não é do YouTube")
            return None
            
        with self._driver_context() as driver:
            try:
                logger.info(f"Acessando URL: {url}")
                driver.get(url)
                
                # Aguarda o título aparecer com múltiplos seletores
                title_selectors = [
                    (By.CSS_SELECTOR, 'h1[class*="ytd-video-primary-info-renderer"] yt-formatted-string'),
                    (By.CSS_SELECTOR, 'h1.ytd-video-primary-info-renderer yt-formatted-string'),
                    (By.XPATH, '//*[@id="container"]/h1/yt-formatted-string'),
                    (By.CSS_SELECTOR, 'h1 yt-formatted-string'),
                    (By.CSS_SELECTOR, '[class*="title"] yt-formatted-string')
                ]
                
                title_element = None
                for selector_type, selector in title_selectors:
                    try:
                        title_element = WebDriverWait(driver, self.timeout).until(
                            EC.presence_of_element_located((selector_type, selector))
                        )
                        break
                    except TimeoutException:
                        continue
                
                if title_element:
                    title = title_element.text.strip()
                    logger.info(f"Título encontrado: {title}")
                    return title
                else:
                    logger.warning("Nenhum título encontrado com os seletores disponíveis")
                    return None
                    
            except TimeoutException:
                logger.error("Timeout ao carregar a página")
                return None
            except WebDriverException as e:
                logger.error(f"Erro do WebDriver: {e}")
                return None
            except Exception as e:
                logger.error(f"Erro inesperado: {e}")
                return None
    
    @staticmethod
    def _is_valid_youtube_url(url):
        """Verifica se a URL é válida do YouTube"""
        youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com']
        return any(domain in url.lower() for domain in youtube_domains)

class ScraperTask:
    """Classe para representar uma tarefa de scraping"""
    
    def __init__(self, task_id: str, url: str, callback=None):
        self.task_id = task_id
        self.url = url
        self.callback = callback
        self.status = "pending"
        self.result = None
        self.error = None
        self.started_at = None
        self.completed_at = None
        self.thread = None

class YouTubeScraperManager:
    """Gerenciador de múltiplas execuções do scraper em background"""
    
    def __init__(self, max_workers: int = 3):
        self.max_workers = max_workers
        self.tasks: Dict[str, ScraperTask] = {}
        self.task_queue = queue.Queue()
        self.worker_threads: List[threading.Thread] = []
        self.is_running = False
        self.lock = threading.Lock()
        self.task_counter = 0
        
        # Configura handler para interrupção se disponível
        try:
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
        except:
            pass  # Ignora se não conseguir configurar signals
    
    def _signal_handler(self, signum, frame):
        """Handler para sinais de interrupção"""
        logger.info(f"Sinal {signum} recebido. Finalizando...")
        self.stop()
        sys.exit(0)
    
    def start(self):
        """Inicia o gerenciador e workers"""
        if self.is_running:
            logger.warning("Gerenciador já está em execução")
            return
        
        self.is_running = True
        logger.info(f"Iniciando gerenciador com {self.max_workers} workers")
        
        # Inicia workers
        for i in range(self.max_workers):
            worker = threading.Thread(
                target=self._worker,
                name=f"Worker-{i+1}",
                daemon=True
            )
            worker.start()
            self.worker_threads.append(worker)
        
        logger.info("Gerenciador iniciado com sucesso")
    
    def stop(self):
        """Para o gerenciador e todos os workers"""
        if not self.is_running:
            return
        
        logger.info("Parando gerenciador...")
        self.is_running = False
        
        # Adiciona tarefas de parada para todos os workers
        for _ in range(self.max_workers):
            try:
                self.task_queue.put(None, timeout=1)
            except:
                pass
        
        # Aguarda workers terminarem
        for worker in self.worker_threads:
            if worker.is_alive():
                worker.join(timeout=5)
        
        self.worker_threads.clear()
        logger.info("Gerenciador parado")
    
    def _worker(self):
        """Worker thread que processa tarefas"""
        scraper = YouTubeVideoScraper(timeout=15)
        
        while self.is_running:
            try:
                # Pega próxima tarefa
                task = self.task_queue.get(timeout=1)
                
                if task is None:  # Sinal de parada
                    break
                
                self._process_task(task, scraper)
                self.task_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Erro no worker: {e}")
    
    def _process_task(self, task: ScraperTask, scraper: YouTubeVideoScraper):
        """Processa uma tarefa de scraping"""
        try:
            with self.lock:
                task.status = "running"
                task.started_at = datetime.now()
            
            logger.info(f"Processando tarefa {task.task_id}: {task.url}")
            
            # Executa o scraping
            result = scraper.get_video_title(task.url)
            
            with self.lock:
                task.status = "completed"
                task.result = result
                task.completed_at = datetime.now()
            
            logger.info(f"Tarefa {task.task_id} concluída: {result}")
            
            # Executa callback se fornecido
            if task.callback:
                try:
                    task.callback(task)
                except Exception as e:
                    logger.error(f"Erro no callback da tarefa {task.task_id}: {e}")
                
        except Exception as e:
            with self.lock:
                task.status = "failed"
                task.error = str(e)
                task.completed_at = datetime.now()
            
            logger.error(f"Tarefa {task.task_id} falhou: {e}")
    
    def add_task(self, url: str, callback=None) -> str:
        """Adiciona uma nova tarefa à fila"""
        with self.lock:
            self.task_counter += 1
            task_id = f"task_{self.task_counter:04d}"
        
        task = ScraperTask(task_id, url, callback)
        
        with self.lock:
            self.tasks[task_id] = task
        
        self.task_queue.put(task)
        logger.info(f"Tarefa {task_id} adicionada à fila")
        
        return task_id
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """Obtém status de uma tarefa"""
        with self.lock:
            task = self.tasks.get(task_id)
            if not task:
                return None
            
            return {
                'task_id': task.task_id,
                'url': task.url,
                'status': task.status,
                'result': task.result,
                'error': task.error,
                'started_at': task.started_at,
                'completed_at': task.completed_at
            }
    
    def get_all_tasks(self) -> List[Dict]:
        """Obtém status de todas as tarefas"""
        with self.lock:
            return [self.get_task_status(task_id) for task_id in self.tasks.keys()]
    
    def clear_completed_tasks(self):
        """Remove tarefas concluídas da memória"""
        with self.lock:
            completed_tasks = [
                task_id for task_id, task in self.tasks.items()
                if task.status in ['completed', 'failed']
            ]
            
            for task_id in completed_tasks:
                del self.tasks[task_id]
            
            logger.info(f"Removidas {len(completed_tasks)} tarefas concluídas")
    
    def get_stats(self) -> Dict:
        """Obtém estatísticas do gerenciador"""
        with self.lock:
            stats = {
                'total_tasks': len(self.tasks),
                'pending': sum(1 for task in self.tasks.values() if task.status == 'pending'),
                'running': sum(1 for task in self.tasks.values() if task.status == 'running'),
                'completed': sum(1 for task in self.tasks.values() if task.status == 'completed'),
                'failed': sum(1 for task in self.tasks.values() if task.status == 'failed'),
                'queue_size': self.task_queue.qsize(),
                'workers_active': len([t for t in self.worker_threads if t.is_alive()]),
                'is_running': self.is_running
            }
        
        return stats

def print_task_result(task):
    """Callback para imprimir resultado da tarefa"""
    print(f"\n{'='*60}")
    print(f"📺 RESULTADO DA TAREFA {task.task_id}")
    print(f"{'='*60}")
    print(f"URL: {task.url}")
    if task.result:
        print(f"✅ Título: {task.result}")
    else:
        print(f"❌ Falha: {task.error or 'Título não encontrado'}")
    if task.started_at and task.completed_at:
        duration = task.completed_at - task.started_at
        print(f"⏱️  Duração: {duration.total_seconds():.2f} segundos")
    print(f"{'='*60}\n")

def main():
    """Função principal com interface interativa"""
    print("🚀 YouTube Scraper Manager")
    print("="*50)
    
    # Inicializa gerenciador
    manager = YouTubeScraperManager(max_workers=3)
    
    try:
        manager.start()
        print("✅ Gerenciador iniciado!")
        print("Digite 'help' para ver os comandos disponíveis")
        
        while True:
            try:
                print("\n" + "-"*30)
                command = input(">>> ").strip().lower()
                
                if command == 'help':
                    print("\n📋 COMANDOS DISPONÍVEIS:")
                    print("  add <url>     - Adiciona nova tarefa")
                    print("  status        - Mostra estatísticas")
                    print("  tasks         - Lista todas as tarefas")
                    print("  clear         - Remove tarefas concluídas")
                    print("  stop          - Para o gerenciador")
                    print("  help          - Mostra esta ajuda")
                
                elif command.startswith('add '):
                    url = command[4:].strip()
                    if url:
                        task_id = manager.add_task(url, callback=print_task_result)
                        print(f"✅ Tarefa {task_id} adicionada à fila")
                    else:
                        print("❌ URL não fornecida")
                
                elif command == 'status':
                    stats = manager.get_stats()
                    print(f"\n📊 ESTATÍSTICAS:")
                    print(f"  Total de tarefas: {stats['total_tasks']}")
                    print(f"  Pendentes: {stats['pending']}")
                    print(f"  Executando: {stats['running']}")
                    print(f"  Concluídas: {stats['completed']}")
                    print(f"  Falharam: {stats['failed']}")
                    print(f"  Fila: {stats['queue_size']}")
                    print(f"  Workers ativos: {stats['workers_active']}")
                    print(f"  Status: {'🟢 Ativo' if stats['is_running'] else '🔴 Inativo'}")
                
                elif command == 'tasks':
                    tasks = manager.get_all_tasks()
                    if tasks:
                        print(f"\n📋 TAREFAS ({len(tasks)}):")
                        for task in tasks[-10:]:  # Últimas 10 tarefas
                            status_emoji = {
                                'pending': '⏳',
                                'running': '🔄',
                                'completed': '✅',
                                'failed': '❌'
                            }.get(task['status'], '❓')
                            
                            url_display = task['url'][:50] + "..." if len(task['url']) > 50 else task['url']
                            print(f"  {status_emoji} {task['task_id']}: {url_display}")
                            
                            if task['result']:
                                result_display = task['result'][:60] + "..." if len(task['result']) > 60 else task['result']
                                print(f"      Título: {result_display}")
                            elif task['error']:
                                print(f"      Erro: {task['error']}")
                    else:
                        print("📭 Nenhuma tarefa encontrada")
                
                elif command == 'clear':
                    manager.clear_completed_tasks()
                    print("✅ Tarefas concluídas removidas")
                
                elif command in ['stop', 'exit', 'quit']:
                    print("🛑 Parando gerenciador...")
                    manager.stop()
                    print("👋 Programa finalizado!")
                    break
                
                elif command == '':
                    continue
                
                else:
                    print("❌ Comando não reconhecido. Digite 'help' para ajuda")
                    
            except KeyboardInterrupt:
                print("\n🛑 Interrompido pelo usuário")
                break
            except EOFError:
                print("\n🛑 Entrada finalizada")
                break
            except Exception as e:
                print(f"❌ Erro: {e}")
                
    except Exception as e:
        logger.error(f"Erro fatal: {e}")
    finally:
        manager.stop()
        print("👋 Sistema finalizado!")

if __name__ == "__main__":
    main()