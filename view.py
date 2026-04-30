# -*- coding: utf-8 -*-
from tkinter import *
import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import threading
import psutil
import time

class Application:
    def __init__(self, master=None):
        self.master = master
        self.fontePadrao = ("Arial", "10")
        self.processos = []
        self.total_visualizacoes = 0
        self.rodando = False
        self.thread_monitor = None
        
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
        self.titulo = Label(self.primeiroContainer, text="Engaja Tube - Visualizador Automático")
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

        self.infoLabel = Label(self.terceiroContainer, text="(Recomendado: 2-5)", font=("Arial", "8"), fg="gray")
        self.infoLabel.pack(side=LEFT)

        # Contador de visualizações
        self.contadorLabel = Label(self.quartoContainer, text="Visualizações totais: 0", font=("Arial", "11", "bold"), fg="blue")
        self.contadorLabel.pack()

        # Status
        self.statusLabel = Label(self.quintoContainer, text="Status: Parado", font=("Arial", "9"), fg="red")
        self.statusLabel.pack()

        # Uso de recursos
        self.recursosLabel = Label(self.quintoContainer, text="CPU: 0% | RAM: 0%", font=("Arial", "8"), fg="gray")
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
            cpu = psutil.cpu_percent(interval=0.1)
            ram = psutil.virtual_memory().percent
            self.recursosLabel["text"] = f"CPU: {cpu:.1f}% | RAM: {ram:.1f}%"
        except:
            pass

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
        """Loop principal que gerencia as instâncias de visualização"""
        while self.rodando:
            try:
                # Verificar recursos antes de criar novas instâncias
                cpu = psutil.cpu_percent(interval=0.1)
                ram = psutil.virtual_memory().percent
                
                if cpu > 90 or ram > 90:
                    print(f"Recursos altos - CPU: {cpu}%, RAM: {ram}% - Aguardando...")
                    time.sleep(5)
                    continue
                
                # Limpar processos finalizados
                self.processos = [p for p in self.processos if p.poll() is None]
                
                # Criar novas instâncias se necessário
                while len(self.processos) < num_instancias and self.rodando:
                    try:
                        processo = subprocess.Popen(
                            ["python", "comandos.py", link],
                            shell=False,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )
                        self.processos.append(processo)
                        self.total_visualizacoes += 1
                        self.master.after(0, self.atualizarContador)
                        print(f"Instância {len(self.processos)} iniciada - Total de visualizações: {self.total_visualizacoes}")
                        time.sleep(2)  # Delay entre instâncias
                    except Exception as e:
                        print(f"Erro ao criar instância: {e}")
                        break
                
                time.sleep(1)
                
            except Exception as e:
                print(f"Erro no loop: {e}")
                time.sleep(5)

    def atualizarRecursosLoop(self):
        """Atualiza recursos periodicamente"""
        if self.rodando:
            self.atualizarRecursos()
            self.master.after(2000, self.atualizarRecursosLoop)

    def pararVisualizacoes(self):
        """Para todas as visualizações"""
        self.rodando = False
        
        # Finalizar todos os processos
        for processo in self.processos:
            try:
                processo.terminate()
                processo.wait(timeout=3)
            except:
                try:
                    processo.kill()
                except:
                    pass
        
        self.processos = []
        self.bt_iniciar["state"] = NORMAL
        self.bt_parar["state"] = DISABLED
        self.statusLabel["text"] = "Status: Parado"
        self.statusLabel["fg"] = "red"
        
        messagebox.showinfo("Parado", f"Visualizações paradas!\nTotal de visualizações iniciadas: {self.total_visualizacoes}")

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
