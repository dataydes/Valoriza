# -*- coding: utf-8 -*-
"""
Exemplo de uso do YouTube Scraper Manager
Demonstra como usar o gerenciador programaticamente
"""

import time
from IA.youtube_scraper_manager import YouTubeScraperManager

def custom_callback(task):
    """Callback personalizado para processar resultados"""
    print(f"🎯 Callback: Tarefa {task.task_id} processada!")
    if task.result:
        # Aqui você pode salvar em banco de dados, arquivo, etc.
        with open('resultados.txt', 'a', encoding='utf-8') as f:
            f.write(f"{task.url} -> {task.result}\n")

def exemplo_uso_programatico():
    """Exemplo de uso programático do gerenciador"""
    
    # Lista de URLs para testar
    urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://www.youtube.com/watch?v=9bZkp7q19f0",
        "https://www.youtube.com/watch?v=kJQP7kiw5Fk",
        "https://www.youtube.com/watch?v=fJ9rUzIMcZQ",
        "https://www.youtube.com/watch?v=ZbZSe6N_BXs"
    ]
    
    # Inicializa gerenciador
    manager = YouTubeScraperManager(max_workers=2)
    manager.start()
    
    try:
        # Adiciona tarefas
        task_ids = []
        for url in urls:
            task_id = manager.add_task(url, callback=custom_callback)
            task_ids.append(task_id)
            print(f"✅ Adicionada tarefa {task_id}")
        
        # Monitora execução
        print("\n📊 Monitorando execução...")
        while True:
            stats = manager.get_stats()
            print(f"Pendentes: {stats['pending']}, Executando: {stats['running']}, Concluídas: {stats['completed']}")
            
            if stats['pending'] == 0 and stats['running'] == 0:
                break
            
            time.sleep(2)
        
        # Mostra resultados finais
        print("\n📋 Resultados finais:")
        for task_id in task_ids:
            status = manager.get_task_status(task_id)
            if status:
                print(f"  {task_id}: {status['result'] or 'FALHA'}")
        
    finally:
        manager.stop()
        print("🛑 Gerenciador finalizado")

def exemplo_execucao_continua():
    """Exemplo de execução contínua com adição dinâmica de tarefas"""
    
    manager = YouTubeScraperManager(max_workers=3)
    manager.start()
    
    print("🔄 Modo de execução contínua iniciado")
    print("Adicione URLs ou digite 'stop' para parar")
    
    try:
        while True:
            url = input("\nDigite uma URL (ou 'stop'): ").strip()
            
            if url.lower() == 'stop':
                break
            
            if url:
                task_id = manager.add_task(url)
                print(f"✅ Tarefa {task_id} adicionada")
                
                # Mostra stats atuais
                stats = manager.get_stats()
                print(f"📊 Fila: {stats['queue_size']}, Ativas: {stats['running']}")
    
    finally:
        manager.stop()

if __name__ == "__main__":
    print("Escolha o modo de execução:")
    print("1. Uso programático (lista predefinida)")
    print("2. Execução contínua (adicionar manualmente)")
    
    choice = input("Escolha (1 ou 2): ").strip()
    
    if choice == "1":
        exemplo_uso_programatico()
    elif choice == "2":
        exemplo_execucao_continua()
    else:
        print("❌ Opção inválida")