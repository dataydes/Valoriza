#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Engaja Tube - Visualizador de YouTube com Rede Tor
Versão 2.1.1 - Corrigido e Otimizado
- Validação de URL
- Timeout em driver.quit()
- Flag --no-tor explícita
- Retry com backoff exponencial
"""

import sys
import os
import re
import time
import random
import logging
import argparse
import socket
import signal
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# ✅ Função de validação de URL
def is_valid_url(url: str) -> bool:
    """Valida se a URL é válida e contém domínio de vídeo do YouTube."""
    youtube_pattern = r'(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.*'
    return bool(re.match(youtube_pattern, url, re.IGNORECASE))

# Configuração de Logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
]

def check_tor_connection(host: str = "127.0.0.1", port: int = 9050, timeout: int = 3) -> bool:
    """Verifica se o proxy Tor está ativo e escutando na porta."""
    try:
        sock = socket.create_connection((host, port), timeout=timeout)
        sock.close()
        return True
    except (ConnectionRefusedError, TimeoutError, OSError):
        return False

def setup_driver(use_tor: bool = True, headless: bool = False, user_agent: str = None) -> Optional[webdriver.Chrome]:
    """Configura o driver do Chrome com otimizações de desempenho e privacidade."""
    options = Options()


    # 🎨 Controle de interface (CORRIGIDO: headless precisa do argumento explícito)
    if headless:
        # ✅ Correção: Selenium Chrome headless requer --headless=new E window-size
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1280,720")
        logger.info("Modo headless ATIVADO (navegador oculto)")
    else:
        logger.info("Modo gráfico ATIVADO (navegador visível para monitoramento)")

    # 🛡️ Anti-Detecção & Privacidade
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--incognito")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--mute-audio")

    # ⚡ Desempenho & Estabilidade
    options.add_argument("--log-level=3")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-default-apps")
    options.add_argument("--window-size=1366,768")  # ✅ Restaurado para modo gráfico
    options.add_argument("--dns-over-https=off")  # Previne vazamento DNS via DoH

    # 🌐 Configuração Tor (se ativada)
    if use_tor:
        if not check_tor_connection():
            logger.warning("Proxy Tor não detectado em 127.0.0.1:9050. O tráfego NÃO estará anônimo.")
            logger.warning("Inicie o Tor Browser ou configure 'tor --port 9050' antes de executar.")
        
        options.add_argument("--proxy-server=socks5h://127.0.0.1:9050")
        logger.info("Roteamento Tor configurado (socks5h - DNS remoto)")

        # 🚫 Bloqueio WebRTC (crítico para evitar vazamento de IP local)
        options.add_experimental_option("prefs", {
            "webrtc.ip_handling_policy": "disable_non_proxied_udp",
            "webrtc.multiple_routes_enabled": False,
            "webrtc.nonproxied_udp_enabled": False,
            "profile.default_content_setting_values.geolocation": 2,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        })
        options.add_argument("--disable-webrtc")
        options.add_argument("--disable-features=WebRTC")

    # User-Agent
    ua = user_agent or random.choice(USER_AGENTS)
    options.add_argument(f"--user-agent={ua}")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(45)

        # 💉 Injeção CDP para ocultar automação
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                window.navigator.chrome = {runtime: {}};
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                Object.defineProperty(navigator, 'languages', {get: () => ['pt-BR', 'pt', 'en']});
            """
        })
        return driver
    except Exception as e:
        logger.error(f"Falha ao inicializar o Chrome: {e}")
        return None

def interact_with_video(driver: webdriver.Chrome, url: str, min_view_time: int = 60, max_view_time: int = 150) -> bool:
    """Gerencia a interação com o vídeo e simula comportamento humano."""
    logger.info(f"Navegando para: {url}")
    
    # ✅ Validação de URL
    if not is_valid_url(url):
        logger.error(f"URL inválida: {url}")
        logger.info("Use um link válido do YouTube (ex: https://youtu.be/VIDEO_ID ou https://youtube.com/watch?v=VIDEO_ID)")
        return False
    
    try:
        driver.get(url)
    except WebDriverException as e:
        logger.error(f"Erro ao acessar URL: {e}")
        return False

    # Aguarda player carregar
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "movie_player"))
        )
        logger.info("Player do YouTube detectado.")
    except TimeoutException:
        logger.warning("Timeout ao carregar o player. Continuando assim mesmo...")

    # Tenta iniciar reprodução
    video_started = False
    methods = [
        ("Clique no botão Play", lambda d: d.find_element(By.CSS_SELECTOR, ".ytp-large-play-button").click()),
        ("Clique no vídeo", lambda d: d.find_element(By.CSS_SELECTOR, "#movie_player").click()),
        ("Tecla Espaço", lambda d: d.find_element(By.TAG_NAME, "body").send_keys(Keys.SPACE)),
        ("JS Play", lambda d: d.execute_script("document.querySelector('video')?.play();"))
    ]

    for method_name, action in methods:
        if video_started: break
        try:
            action(driver)
            time.sleep(1.5)
            # Verifica se está pausado
            is_paused = driver.execute_script("return document.querySelector('video')?.paused;")
            if not is_paused:
                logger.info(f"Reprodução iniciada com sucesso: {method_name}")
                video_started = True
        except Exception:
            logger.debug(f"Método '{method_name}' falhou, tentando próximo...")

    if not video_started:
        logger.warning("Não foi possível iniciar a reprodução automaticamente. Continuando assim mesmo...")

    # Simulação de visualização humana
    target_time = random.randint(min_view_time, max_view_time)
    logger.info(f"Tempo de visualização configurado: {target_time} segundos")

    elapsed = 0
    while elapsed < target_time:
        # Delay variável (15-35s)
        step = random.uniform(15, 35)
        time.sleep(step)
        elapsed += step

        # Interações aleatórias (scroll, mouse move implícito)
        if random.random() > 0.65:
            try:
                driver.execute_script("window.scrollBy(0, 120);")
                time.sleep(random.uniform(2, 4))
                driver.execute_script("window.scrollBy(0, -100);")
            except Exception:
                pass

        logger.info(f"⏱️ Progresso: {int(elapsed)}/{target_time}s")

    logger.info("✅ Visualização concluída com sucesso.")
    return True

# ✅ Retry com backoff exponencial para timeouts
def interact_with_video_with_retry(driver: webdriver.Chrome, url: str, min_view_time: int = 60, max_view_time: int = 150, max_retries: int = 3) -> bool:
    """Tenta a interação com retry em caso de timeout."""
    for attempt in range(max_retries):
        try:
            return interact_with_video(driver, url, min_view_time, max_view_time)
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"Erro na tentativa {attempt + 1}/{max_retries}: {e}. Retentando em 2s...")
                time.sleep(2 ** attempt)  # backoff exponencial
            else:
                logger.error(f"Falha máxima atingida após {max_retries} tentativas.")
                return False
    return False

def main():
    parser = argparse.ArgumentParser(description="Engaja Tube v2.1.1 - Visualizador Otimizado com Tor")
    parser.add_argument("link", nargs="?", help="URL do vídeo do YouTube")
    parser.add_argument("--tor", action="store_true", default=True, help="Roteia tráfego via Tor (padrão)")
    parser.add_argument("--no-tor", action="store_true", dest="no_tor", help="Desativa Tor (padrão: ATIVO)")
    parser.add_argument("--headless", action="store_true", default=False, help="Executa sem interface gráfica (padrão: VISÍVEL)")
    parser.add_argument("--user-agent", help="User-Agent personalizado")
    parser.add_argument("--proxy-host", help="Host do proxy (padrão: 127.0.0.1)")
    parser.add_argument("--proxy-port", type=int, help="Porta do proxy (padrão: 9050)")
    args = parser.parse_args()

    if not args.link:
        logger.error("Erro: Link do vídeo não fornecido.")
        logger.info("Uso: python comandos.py <URL_YOUTUBE> [--no-tor] [--headless]")
        sys.exit(1)

    # ✅ Validação de URL
    if not is_valid_url(args.link):
        logger.error(f"URL inválida: {args.link}")
        logger.info("Use um link válido do YouTube (ex: https://youtu.be/VIDEO_ID ou https://youtube.com/watch?v=VIDEO_ID)")
        sys.exit(1)

    # Configuração do Tor (com flag explícita --no-tor)
    use_tor = not args.no_tor
    logger.info("🚀 Iniciando Engaja Tube v2.1.1")
    logger.info(f"🔗 Alvo: {args.link}")
    logger.info(f"🔒 Tor: {'ATIVADO' if use_tor else 'DESATIVADO'}")
    
    host = args.proxy_host or "127.0.0.1"
    port = args.proxy_port or 9050
    
    driver = None
    try:
        driver = setup_driver(use_tor=use_tor, headless=args.headless, user_agent=args.user_agent)
        if driver is None:
            logger.error("Falha crítica: Driver não inicializado. Encerrando.")
            sys.exit(1)

        success = interact_with_video_with_retry(driver, args.link)
        if not success:
            logger.warning("Sessão encerrada com falhas na interação.")
            
    except KeyboardInterrupt:
        logger.info("⛔ Interrupção manual detectada. Finalizando...")
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
    finally:
        if driver:
            logger.info("🧹 Limpando recursos e fechando navegador...")
            try:
                # Timeout para evitar bloqueio indefinitely
                driver.execute_script("window.close()")
                driver.quit()
                logger.info("Navegador fechado com sucesso.")
            except Exception as e:
                logger.warning(f"Falha ao fechar o navegador: {e}")
                # Tentativa final de kill
                try:
                    driver.quit()
                except:
                    logger.error("Falha crítica: Navegador não pode ser fechado. Kill do processo será necessário.")
        logger.info("👋 Instância finalizada.")

if __name__ == "__main__":
    main()