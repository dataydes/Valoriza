# -*- coding: utf-8 -*-
from tkinter import *
import tkinter as tk
import os #comando para o shell
import subprocess #chamada para background
class Application:
    def __init__(self, master=None):
        self.fontePadrao = ("Arial", "10")
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.quartoContainer = Frame(master)
        self.quartoContainer["pady"] = 20
        self.quartoContainer.pack(fill=BOTH)

        self.titulo = Label(self.primeiroContainer, text="Engaja tube")
        self.titulo["font"] = ("Arial", "10", "bold")
        self.titulo.pack()

        self.nomeLabel = Label(self.segundoContainer,text="Insira o link ao vivo", font=self.fontePadrao)
        self.nomeLabel.pack(side=LEFT)

        self.nome = Entry(self.segundoContainer)
        self.nome["width"] = 60
        self.nome["font"] = self.fontePadrao
        self.nome.pack(side=LEFT)

        self.autenticar = Button(self.quartoContainer)
        self.autenticar["text"] = "Gravar"
        self.autenticar["font"] = ("Calibri", "8")
        self.autenticar["width"] = 12
        self.autenticar["command"] = self.chamaGravar
        self.autenticar.pack(side=TOP)

        self.bt_sair = Button(self.quartoContainer)
        self.bt_sair["text"] = "Sair"
        self.bt_sair["font"] = ("Calibri", "8")
        self.bt_sair["width"] = 12
        self.bt_sair["command"] = self.chamaSair
        self.bt_sair.pack(side=RIGHT, padx=20)
        

    #Método chama software
    def chamaGravar(self):
        link = self.nome.get()
        if (link != ""):
            subprocess.Popen(["python", "comandos.py ", link], shell=True)
            
        else:
            self.nomeLabel["font"] = ("Calibri","20")
        return None
    
    def chamaSair(self):
        root.destroy()
        return None


root = tk.Tk()
root.title("Engaja tube")
#root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='./src/elza.png'))
root.iconbitmap(default='./src/icon.ico')
Application(root)
root.mainloop()