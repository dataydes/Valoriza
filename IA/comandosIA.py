# -*- coding: utf-8 -*-
"""
YouTube Video Title Scraper - Versão Otimizada
Extrai o título de vídeos do YouTube de forma eficiente e robusta
"""

import sys
import logging
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
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

def main():
    """Função principal do programa"""
    if len(sys.argv) != 2:
        print("Uso: python script.py <URL_DO_VIDEO>")
        print("Exemplo: python script.py https://www.youtube.com/watch?v=VIDEO_ID")
        sys.exit(1)
    
    url = sys.argv[1]
    
    scraper = YouTubeVideoScraper(timeout=15)
    
    print("🔍 Buscando informações do vídeo...")
    title = scraper.get_video_title(url)
    
    if title:
        print(f"✅ Título encontrado: {title}")
        
        # Menu interativo simplificado
        while True:
            print("\n" + "="*50)
            print("Opções:")
            print("1. Mostrar título novamente")
            print("2. Sair")
            print("="*50)
            
            choice = input("Escolha uma opção (1-2): ").strip()
            
            if choice == '1':
                print(f"📺 Título: {title}")
            elif choice == '2':
                print("👋 Programa finalizado!")
                break
            else:
                print("❌ Opção inválida. Tente novamente.")
    else:
        print("❌ Não foi possível encontrar o vídeo.")
        print("Verifique se:")
        print("  • A URL está correta")
        print("  • O vídeo existe e está público")
        print("  • Você tem conexão com a internet")
        sys.exit(1)

if __name__ == "__main__":
    main()