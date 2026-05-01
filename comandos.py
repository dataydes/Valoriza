# -*- coding: utf-8 -*-
import sys
import time
import random
import argparse
from requests import options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options

# Lista de User-Agents para simular diferentes navegadores/localizações
USER_AGENTS = [
    # EUA
    ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", "Google Chrome Windows (EUA)"),
    ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15", "Safari macOS (EUA)"),
    
    # Reino Unido
    ("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0", "Firefox Windows (UK)"),
    ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15", "Safari macOS (UK)"),
    
    # Alemanha
    ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", "Chrome Linux (DE)"),
    
    # Japão
    ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1", "Safari iOS (Japão)"),
    
    # Austrália
    ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", "Chrome Windows (AU)"),
    
    # Canadá
    ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", "Chrome macOS (CA)"),
]

# Proxies públicos por região (substitua por sua lista de proxies)
PROXIES_REGIONAL = {
    "EUA": {
        "http": "http://proxy-usuario:senha@proxy-eua:8080",
        "https": "https://proxy-usuario:senha@proxy-eua:8080"
    },
    "Reino Unido": {
        "http": "http://proxy-usuario:senha@proxy-uk:8080",
        "https": "https://proxy-usuario:senha@proxy-uk:8080"
    },
    "Alemanha": {
        "http": "http://proxy-usuario:senha@proxy-de:8080",
        "https": "https://proxy-usuario:senha@proxy-de:8080"
    },
    "França": {
        "http": "http://proxy-usuario:senha@proxy-fr:8080",
        "https": "https://proxy-usuario:senha@proxy-fr:8080"
    },
    "Japão": {
        "http": "http://proxy-usuario:senha@proxy-jp:8080",
        "https": "https://proxy-usuario:senha@proxy-jp:8080"
    },
    "Austrália": {
        "http": "http://proxy-usuario:senha@proxy-au:8080",
        "https": "https://proxy-usuario:senha@proxy-au:8080"
    },
    "Canadá": {
        "http": "http://proxy-usuario:senha@proxy-ca:8080",
        "https": "https://proxy-usuario:senha@proxy-ca:8080"
    },
}


def finalizar(driver):
    """Finaliza o driver do navegador"""
    try:
        driver.quit()
    except:
        pass


def setup_driver(proxy=None, user_agent=None):
    """Configura o driver do Chrome com as opções necessárias"""
    options = Options()
    
    # Configurações para evitar detecção
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--mute-audio')
    options.add_argument('window-size=1920x1080')
    options.add_argument('--headless=new')
    options.add_argument('--log-level=3')
    
    # Configura User-Agent (opcional)
    if user_agent:
        options.add_argument(f"--user-agent={user_agent}")
    
    # Configura proxy (opcional)
    if proxy:
        # Remove o proxy padrão do Selenium que pode interferir
        options._properties["proxy"] = {
            "proxyType": "manual",
            "proxyBypassList": [
                "<local>",
                "*.local",
                "127.0.0.1",
                "localhost"
            ],
            "httpProxy": proxy,
            "httpsProxy": proxy
        }
    
    # Preferências adicionais para economizar recursos
    prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_setting_values.media_stream": 2,
        "profile.default_content_setting_values.images": 2,
        "profile.managed_default_content_settings.images": 2,
    }
    options.add_experimental_option("prefs", prefs)
    
    # Inicializar o driver
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver


def main():
    # Configurar parser de argumentos
    parser = argparse.ArgumentParser(description="Visualizador de YouTube com suporte a proxies")
    parser.add_argument("link", nargs="?", help="URL do vídeo do YouTube")
    parser.add_argument("--proxy", help="Proxy HTTP para usar (ex: http://usuario:senha@proxy:8080)")
    parser.add_argument("--user-agent", help="User-Agent para simular localização (ex: Google Chrome Windows)")
    parser.add_argument("--region", help="Região simulada (EUA, UK, DE, JP, etc)")
    parser.add_argument("--ip", help="IP público simulado (pasta alternativa)")
    
    args = parser.parse_args()
    
    # Verifica se foi fornecido um link
    if not args.link:
        print("Erro: Link do vídeo não fornecido")
        print("Uso: python comandos.py <link> [--proxy <url>] [--user-agent <ua>] [--region <nome>]")
        return
    
    proxy = args.proxy or ""
    user_agent = args.user_agent or ""
    region = args.region or None
    
    print(f"Iniciando visualização: {args.link}")
    
    # Configura user-agent se não foi fornecido explicitamente
    if not user_agent and region:
        # Pega user-agent padrão baseado na região
        region_abbreviations = {
            "EUA": "Google Chrome Windows",
            "UK": "Firefox Windows",
            "DE": "Chrome Linux",
            "JP": "Safari iOS",
            "AU": "Chrome Windows",
            "CA": "Chrome macOS",
            "FR": "Firefox Linux"
        }
        ua_name = region_abbreviations.get(region.upper(), "Google Chrome Windows")
        user_agent = next((ua for ua, name in USER_AGENTS if ua_name in name), USER_AGENTS[0][0])
        print(f"User-Agent padrão para {region}: {user_agent}")
    
    # Configura proxy baseado na região se fornecido
    if region:
        if region in PROXIES_REGIONAL:
            print(f"Proxy para {region} configurado (substitua com seu proxy real): {PROXIES_REGIONAL[region]['http']}")
            # Substitua o proxy placeholder com um real se fornecido
            if proxy:
                print(f"Proxy customizado fornecido: {proxy}")
            else:
                print("Atenção: Substitua o proxy placeholder com um proxy real para esta região")
    
    # Configura driver
    try:
        driver = setup_driver(proxy=proxy if proxy else None, user_agent=user_agent if user_agent else None)
        driver.set_page_load_timeout(30)
        
        # Acessar o vídeo
        print("Acessando vídeo...")
        driver.get(args.link)
        
        # Aguardar carregamento da página
        time.sleep(5)
        
        # Tentar iniciar o vídeo de várias formas
        video_iniciado = False
        
        # Método 1: Clicar no botão de play
        try:
            wait = WebDriverWait(driver, 10)
            play_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ytp-large-play-button")))
            play_button.click()
            print("Vídeo iniciado (método 1)")
            video_iniciado = True
        except:
            print("Método 1 falhou, tentando método 2...")
        
        # Método 2: Usar tecla de atalho
        if not video_iniciado:
            try:
                from selenium.webdriver.common.keys import Keys
                video_element = driver.find_element(By.TAG_NAME, "video")
                video_element.click()
                time.sleep(1)
                video_element.send_keys(Keys.SPACE)
                print("Vídeo iniciado (método 2)")
                video_iniciado = True
            except:
                print("Método 2 falhou, tentando método 3...")
        
        # Método 3: JavaScript
        if not video_iniciado:
            try:
                driver.execute_script("document.querySelector('video').play();")
                print("Vídeo iniciado (método 3 - JavaScript)")
                video_iniciado = True
            except:
                print("Método 3 falhou")
        
        if not video_iniciado:
            print("Aviso: Não foi possível iniciar o vídeo automaticamente")
        
        # Simular comportamento humano - tempo de visualização aleatório
        tempo_visualizacao = random.randint(30, 120)  # Entre 30 segundos e 2 minutos
        print(f"Visualizando por {tempo_visualizacao} segundos...")
        
        # Aguardar e simular interações ocasionais
        tempo_decorrido = 0
        while tempo_decorrido < tempo_visualizacao:
            time.sleep(random.uniform(8, 15))  # Delay variável
            tempo_decorrido += random.uniform(8, 15)
            
            # Ocasionalmente simular scroll ou movimento
            if random.random() > 0.6:
                try:
                    driver.execute_script("window.scrollBy(0, 150);")
                    time.sleep(random.uniform(1, 2))
                except:
                    pass
        
        print(f"Visualização concluída após {int(tempo_decorrido)} segundos")
        print(f"IP/Região simulada: {region or 'Nenhum'}")
        
    except TimeoutException:
        print("Erro: Timeout ao carregar o vídeo")
    except Exception as e:
        print(f"Erro durante execução: {str(e)}")
    finally:
        # Sempre finalizar o driver
        if driver:
            finalizar(driver)
        print("Instância finalizada")


if __name__ == "__main__":
    main()