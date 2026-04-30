# -*- coding: utf-8 -*-
import sys
import time
import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def finalizar(driver):
    """Finaliza o driver do navegador"""
    try:
        driver.quit()
    except:
        pass

def main():
    driver = None
    try:
        # Recupera o link do vídeo
        if len(sys.argv) < 2:
            print("Erro: Link do vídeo não fornecido")
            return
        
        link = sys.argv[1]
        print(f"Iniciando visualização: {link}")
        
        # Configurações do Chrome para otimização
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--mute-audio')  # Silenciar áudio
        options.add_argument('window-size=800x600')
        options.add_argument('--log-level=3')  # Reduzir logs
        
        # Modo headless opcional (descomente para economizar recursos)
        # options.add_argument('--headless')
        
        # Preferências adicionais para economizar recursos
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_setting_values.media_stream": 2,
        }
        options.add_experimental_option("prefs", prefs)
        
        # Inicializar o driver
        service = ChromeService(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(30)
        
        # Acessar o vídeo
        print("Acessando vídeo...")
        driver.get(link)
        
        # Aguardar carregamento da página
        time.sleep(3)
        
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
                video_element = driver.find_element(By.TAG_NAME, "video")
                video_element.click()
                time.sleep(1)
                # Pressionar 'k' para play/pause
                from selenium.webdriver.common.keys import Keys
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
            time.sleep(10)
            tempo_decorrido += 10
            
            # Ocasionalmente simular scroll ou movimento
            if random.random() > 0.7:
                try:
                    driver.execute_script("window.scrollBy(0, 100);")
                except:
                    pass
        
        print(f"Visualização concluída após {tempo_visualizacao} segundos")
        
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
