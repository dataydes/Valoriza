# -*- coding: utf-8 -*-
"""
Script de teste simples para o YouTube Scraper Manager
"""

import time
import sys
import os

# Adiciona o diretório atual ao path se necessário
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_manager():
    """Testa o gerenciador com URLs de exemplo"""
    
    try:
        # Importa o gerenciador
        from IA.youtube_scraper_manager import YouTubeScraperManager
        
        # URLs de teste
        test_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll
            "https://www.youtube.com/watch?v=9bZkp7q19f0",  # PSY - Gangnam Style
            "https://www.youtube.com/watch?v=kJQP7kiw5Fk",  # Luis Fonsi - Despacito
        ]
        
        print("🧪 Iniciando teste do sistema...")
        
        # Cria o gerenciador
        manager = YouTubeScraperManager(max_workers=2)
        manager.start()
        
        # Adiciona tarefas
        print("\n📋 Adicionando tarefas...")
        task_ids = []
        for i, url in enumerate(test_urls, 1):
            task_id = manager.add_task(url)
            task_ids.append(task_id)
            print(f"✅ Tarefa {i}: {task_id} adicionada")
        
        # Monitora execução
        print("\n🔄 Monitorando execução...")
        while True:
            stats = manager.get_stats()
            print(f"📊 Pendentes: {stats['pending']}, Executando: {stats['running']}, Concluídas: {stats['completed']}, Falharam: {stats['failed']}")
            
            # Para quando todas as tarefas terminarem
            if stats['pending'] == 0 and stats['running'] == 0 and stats['total_tasks'] > 0:
                break
                
            time.sleep(2)
        
        # Mostra resultados
        print("\n📋 RESULTADOS FINAIS:")
        print("=" * 60)
        for task_id in task_ids:
            status = manager.get_task_status(task_id)
            if status:
                print(f"\n🎯 {task_id}:")
                print(f"   URL: {status['url']}")
                print(f"   Status: {status['status']}")
                if status['result']:
                    print(f"   ✅ Título: {status['result']}")
                else:
                    print(f"   ❌ Erro: {status['error'] or 'Desconhecido'}")
                
                if status['started_at'] and status['completed_at']:
                    duration = status['completed_at'] - status['started_at']
                    print(f"   ⏱️  Duração: {duration.total_seconds():.2f}s")
        
        print("\n" + "=" * 60)
        print("🎉 Teste concluído!")
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("Certifique-se de que o arquivo youtube_scraper_manager.py está no mesmo diretório")
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
    finally:
        try:
            manager.stop()
        except:
            pass

def interactive_test():
    """Teste interativo simples"""
    
    try:
        from IA.youtube_scraper_manager import YouTubeScraperManager
        
        print("🎮 Modo de teste interativo")
        print("Digite URLs do YouTube ou 'quit' para sair")
        
        manager = YouTubeScraperManager(max_workers=1)
        manager.start()
        
        while True:
            try:
                url = input("\n🔗 URL: ").strip()
                
                if url.lower() in ['quit', 'exit', 'q']:
                    break
                
                if url:
                    task_id = manager.add_task(url)
                    print(f"✅ Tarefa {task_id} adicionada")
                    
                    # Aguarda um pouco e mostra resultado
                    time.sleep(1)
                    
                    # Monitora até completar
                    max_wait = 30  # 30 segundos máximo
                    waited = 0
                    while waited < max_wait:
                        status = manager.get_task_status(task_id)
                        if status and status['status'] in ['completed', 'failed']:
                            break
                        time.sleep(1)
                        waited += 1
                    
                    # Mostra resultado
                    status = manager.get_task_status(task_id)
                    if status:
                        if status['result']:
                            print(f"🎯 Título: {status['result']}")
                        else:
                            print(f"❌ Erro: {status['error'] or 'Não encontrado'}")
                    
            except KeyboardInterrupt:
                print("\n🛑 Interrompido")
                break
            except Exception as e:
                print(f"❌ Erro: {e}")
        
        manager.stop()
        print("👋 Teste finalizado!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    print("🚀 Script de Teste - YouTube Scraper Manager")
    print("=" * 50)
    print("Escolha o modo de teste:")
    print("1. Teste automático (URLs predefinidas)")
    print("2. Teste interativo (digite URLs)")
    print("3. Sair")
    
    while True:
        try:
            choice = input("\nEscolha (1-3): ").strip()
            
            if choice == "1":
                test_manager()
                break
            elif choice == "2":
                interactive_test()
                break
            elif choice == "3":
                print("👋 Saindo...")
                break
            else:
                print("❌ Opção inválida. Escolha 1, 2 ou 3.")
                
        except KeyboardInterrupt:
            print("\n👋 Saindo...")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")
            break