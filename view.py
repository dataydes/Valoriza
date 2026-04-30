# -*- coding: utf-8 -*-
"""
Engaja Tube - Visualizador Automático Otimizado
Versão 2.0.3 - Terminal Logs Enabled
"""
from tkinter import *
import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import threading
import psutil
import time
import random

class Application:
    def __init__(self, master=None):
        self.master = master
        self.fontePadrao = ("Arial", "10")
        self.processos = []
        self.total_visualizacoes = 0
        self.rodando = False
        
        # Containers
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer["pady"] = 10
        self.terceiroContainer.pack()

        self.quartoContainer = Frame(master)
        self.quartoContainer["pady"] = 10
        self.quartoContainer.pack()

        self.quintoContainer = Frame(master)
        self.quintoContainer["pady"] = 10
        self.quintoContainer.pack()

        self.sextoContainer = Frame(master)
        self.sextoContainer["pady"] = 20
        self.sextoContainer.pack(fill=BOTH)

        # Título
        self.titulo = Label(self.primeiroContainer, text="Engaja Tube - Visualizador Automático (Otimizado v2.0.3)")
        self.titulo["font"] = ("Arial", "12", "bold")
        self.titulo.pack()

        # Link do vídeo
        self.nomeLabel = Label(self.segundoContainer, text="Link do vídeo:", font=self.fontePadrao)
        self.nomeLabel.pack(side=LEFT)

        self.nome = Entry(self.segundoContainer)
        self.nome["width"] = 60
        self.nome["font"] = self.fontePadrao
        self.nome.pack(side=LEFT)

        # Número de instâncias
        self.instanciasLabel = Label(self.terceiroContainer, text="Instâncias simultâneas:", font=self.fontePadrao)
        self.instanciasLabel.pack(side=LEFT)

        self.instancias = Spinbox(self.terceiroContainer, from_=1, to=20, width=10, font=self.fontePadrao)
        self.instancias.delete(0, END)
        self.instancias.insert(0, "3")
        self.instancias.pack(side=LEFT, padx=5)

        self.infoLabel = Label(self.terceiroContainer, text="(Recomendado: 2-5 instâncias)", font=("Arial", 8), fg="gray")
        self.infoLabel.pack(side=LEFT)

        # Contador de visualizações
        self.contadorLabel = Label(self.quartoContainer, text="Visualizações totais: 0", font=("Arial", 11, "bold"), fg="blue")
        self.contadorLabel.pack()

        # Status
        self.statusLabel = Label(self.quintoContainer, text="Status: Parado", font=("Arial", 9), fg="red")
        self.statusLabel.pack()

        # Uso de recursos
        self.recursosLabel = Label(self.quintoContainer, text="CPU: 0% | RAM: 0%", font=("Arial", 8), fg="gray")
        self.recursosLabel.pack()

        # Botões
        self.bt_iniciar = Button(self.sextoContainer)
        self.bt_iniciar["text"] = "Iniciar Visualizações"
        self.bt_iniciar["font"] = ("Calibri", "10", "bold")
        self.bt_iniciar["width"] = 20
        self.bt_iniciar["bg"] = "#4CAF50"
        self.bt_iniciar["fg"] = "white"
        self.bt_iniciar["command"] = self.iniciarVisualizacoes
        self.bt_iniciar.pack(side=LEFT, padx=10)

        self.bt_parar = Button(self.sextoContainer)
        self.bt_parar["text"] = "Parar"
        self.bt_parar["font"] = ("Calibri", "10", "bold")
        self.bt_parar["width"] = 15
        self.bt_parar["bg"] = "#f44336"
        self.bt_parar["fg"] = "white"
        self.bt_parar["command"] = self.pararVisualizacoes
        self.bt_parar["state"] = DISABLED
        self.bt_parar.pack(side=LEFT, padx=10)

        self.bt_sair = Button(self.sextoContainer)
        self.bt_sair["text"] = "Sair"
        self.bt_sair["font"] = ("Calibri", "10")
        self.bt_sair["width"] = 12
        self.bt_sair["command"] = self.chamaSair
        self.bt_sair.pack(side=LEFT, padx=10)

    def atualizarContador(self):
        """Atualiza o contador de visualizações na interface"""
        self.contadorLabel["text"] = f"Visualizações totais: {self.total_visualizacoes}"
    
    def atualizarRecursos(self):
        """Atualiza informações de uso de recursos"""
        try:
            # Otimização: Usar 0.1s para leitura mais rápida
            cpu = psutil.cpu_percent(interval=0.1)
            mem = psutil.virtual_memory()
            ram = mem.percent
            # Adicionar indicador de status do CPU
            cpu_color = "green" if cpu < 50 else ("yellow" if cpu < 80 else "red")
            self.recursosLabel["fg"] = cpu_color
            self.recursosLabel["text"] = f"CPU: {cpu:.1f}% | RAM: {ram:.1f}% | Memória: {mem.available / (1024**2):.0f}MB"
        except Exception as e:
            self.recursosLabel["text"] = f"Erro: {e}"

    def iniciarVisualizacoes(self):
        """Inicia o processo de visualizações automáticas"""
        link = self.nome.get().strip()
        
        if not link:
            messagebox.showwarning("Aviso", "Por favor, insira o link do vídeo!")
            return
        
        if not link.startswith("http"):
            messagebox.showwarning("Aviso", "Por favor, insira um link válido!")
            return
        
        try:
            num_instancias = int(self.instancias.get())
            if num_instancias < 1 or num_instancias > 20:
                messagebox.showwarning("Aviso", "Número de instâncias deve estar entre 1 e 20!")
                return
        except:
            messagebox.showwarning("Aviso", "Número de instâncias inválido!")
            return
        
        # Verificar recursos disponíveis
        ram_disponivel = psutil.virtual_memory().available / (1024**3)  # GB
        if ram_disponivel < 2:
            if not messagebox.askyesno("Aviso", f"RAM disponível baixa ({ram_disponivel:.1f}GB). Continuar?"):
                return
        
        self.rodando = True
        self.bt_iniciar["state"] = DISABLED
        self.bt_parar["state"] = NORMAL
        self.statusLabel["text"] = "Status: Executando"
        self.statusLabel["fg"] = "green"
        
        # Iniciar thread de monitoramento
        self.thread_monitor = threading.Thread(target=self.executarLoop, args=(link, num_instancias), daemon=True)
        self.thread_monitor.start()
        
        # Iniciar atualização de recursos
        self.atualizarRecursosLoop()

    def executarLoop(self, link, num_instancias):
        """
        Loop principal otimizado que gerencia as instâncias de visualização
        
        Args:
            link: URL do vídeo a ser reproduzido
            num_instancias: Número máximo de instâncias simultâneas
        """
        # Cache do link para evitar re-encoding
        link_normalized = link.strip().lower()
        
        while self.rodando:
            try:
                # Verificar recursos - Otimização: Delay variável para evitar sincronização
                cpu = psutil.cpu_percent(interval=0.1)
                mem = psutil.virtual_memory()
                ram = mem.percent
                ram_mb = mem.available / (1024**2)
                
                # Ajuste inteligente baseado em recursos
                if cpu > 90 or ram > 90:
                    # Delay variável para evitar sincronização
                    time.sleep(random.uniform(3, 6))
                    continue
                elif cpu > 75 or ram > 85:
                    # Delay mais curto para permitir recuperação
                    time.sleep(random.uniform(1, 3))
                
                # Otimização: Limpeza eficiente de processos com slice
                self.processos[:] = [p for p in self.processos if p.poll() is None]
                
                # Criar novas instâncias apenas quando necessário
                slots_livres = num_instancias - len(self.processos)
                
                if slots_livres > 0 and self.rodando and ram_mb >= 500:
                    # Otimização: Criar instâncias em lotes para reduzir bloqueio
                    batch_size = min(slots_livres, 3)  # Máximo 3 por lote
                    
                    for _ in range(batch_size):
                        if not self.rodando or ram_mb < 500:
                            break
                        
                        try:
                            # Habilitar logs no terminal para visualização do progresso
                            processo = subprocess.Popen(
                                ["python", "comandos.py", link],
                                shell=False,
                                stdout=None,  # Mantém stdout habilitado para logs no terminal
                                stderr=None,  # Mantém stderr habilitado para erros no terminal
                                creationflags=subprocess.CREATE_NO_WINDOW
                            )
                            self.processos.append(processo)
                            self.total_visualizacoes += 1
                            
                            # Mensagem de log no terminal para cada instância
                            print(f"[{time.strftime('%H:%M:%S')}] >>> Nova instância iniciada | ID: {len(self.processos)} | Total: {self.total_visualizacoes}")
                            try:
                                self.master.after(500, self.atualizarContador)
                            except:
                                pass
                        
                        except Exception as e:
                            print(f"[{time.strftime('%H:%M:%S')}] Erro ao criar instância: {e}")
                            continue

                # Otimização: Delay variável para evitar sincronização de processos
                delay = random.uniform(0.5, 1.5)
                time.sleep(delay)
                
                # Checkpoint: Atualização da UI periodicamente
                if self.total_visualizacoes % 50 == 0:
                    try:
                        self.master.after(500, self.atualizarContador)
                        print(f"[{time.strftime('%H:%M:%S')}] >>> Atualizando interface (cada 50 visualizações)")
                    except:
                        pass

            except Exception as e:
                print(f"[{time.strftime('%H:%M:%S')}] Erro no loop: {e}")
                # Delay mais longo em caso de erro
                time.sleep(random.uniform(2, 5))
                
                # Otimização: Delay variável entre atualizações de recursos
                delay = random.uniform(1.5, 2.5)
                print(f"[{time.strftime('%H:%M:%S')}] >>> Recurso Monitor: CPU {cpu:.1f}% | RAM {ram:.1f}%")
                self.master.after(int(delay * 1000), self.atualizarRecursosLoop)
                
                # Otimização: Delay variável para evitar sincronização de processos
                delay = random.uniform(0.5, 1.5)
                time.sleep(delay)
                
                # Checkpoint: Atualização da UI periodicamente
                if self.total_visualizacoes % 50 == 0:
                    try:
                        self.master.after(500, self.atualizarContador)
                    except:
                        pass

            except Exception as e:
                print(f"[{time.strftime('%H:%M:%S')}] Erro no loop: {e}")
                # Delay mais longo em caso de erro
                time.sleep(random.uniform(2, 5))

    def atualizarRecursosLoop(self):
        """Atualiza recursos periodicamente com otimização de delay"""
        if self.rodando:
            self.atualizarRecursos()
            # Otimização: Delay variável entre atualizações
            delay = random.uniform(1.5, 2.5)
            self.master.after(int(delay * 1000), self.atualizarRecursosLoop)

    def pararVisualizacoes(self):
        """
        Para todas as visualizações com finalização otimizada
        
        Garante limpeza completa de recursos e processos
        """
        self.rodando = False
        
        # Finalizar todos os processos com tratamento robusto
        processos_ativos = []
        for processo in self.processos:
            if processo.poll() is None:  # Processos ativos
                processos_ativos.append(processo)
        
        print(f"[{time.strftime('%H:%M:%S')}] >>> Finalizando {len(processos_ativos)} processos ativos...")
        
        # Finalização em lotes para evitar travamento
        for lote in range(0, len(processos_ativos), 5):
            batch = processos_ativos[lote:lote + 5]
            for processo in batch:
                processo.terminate()
                # Esperar com timeout progressivo
                for timeout in [2, 3, 5]:
                    try:
                        processo.wait(timeout=timeout)
                        print(f"[{time.strftime('%H:%M:%S')}]   Processo finalizado com timeout={timeout}s")
                        break
                    except subprocess.TimeoutExpired:
                        processo.kill()
                        print(f"[{time.strftime('%H:%M:%S')}]   Processo finalizado com kill (timeout={timeout}s")
        
        # Coleta de garbage para liberar memória
        import gc
        gc.collect()
        
        self.processos = []
        self.bt_iniciar["state"] = NORMAL
        self.bt_parar["state"] = DISABLED
        self.statusLabel["text"] = "Status: Parado"
        self.statusLabel["fg"] = "red"
        
        messagebox.showinfo(
            "Parado",
            f"Visualizações paradas!\n"
            f"Total de visualizações iniciadas: {self.total_visualizacoes}\n"
            f"Processos finalizados com sucesso."
        )

    def chamaSair(self):
        """Fecha o aplicativo"""
        if self.rodando:
            if messagebox.askyesno("Confirmar", "Há visualizações em andamento. Deseja realmente sair?"):
                self.pararVisualizacoes()
                self.master.destroy()
        else:
            self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Engaja Tube - Visualizador Automático")
    root.geometry("600x400")
    try:
        root.iconbitmap(default='./src/icon.ico')
    except:
        pass
    
    app = Application(root)
    root.protocol("WM_DELETE_WINDOW", app.chamaSair)
    root.mainloop()