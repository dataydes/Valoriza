# -*- coding: utf-8 -*-
from logging import error
import sys #coleta o link
import time
from urllib import request, parse
from warnings import catch_warnings #biblioteca da url
from selenium import webdriver #Coleta o nome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

import os #comando para o shell

def finalizar():
	driver.close()
	driver.quit()
	return None

arg = sys.argv[1] #Recupera a variável de entrada
print ("Buscando vídeo")
arg2 = int(sys.argv[2]) #Recupera a variável de entrada

#Coleta dados do browser
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument('window-size=800x600')
#options.add_argument('--headless')
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

#acessando dados
try:
	driver.get(arg)	
	try:
		play = driver.find_element(By.CLASS_NAME,"ytp-play-button ytp-button").click()
	except:
		play1 = driver.find_element(By.CLASS_NAME,"ytp-large-play-button ytp-button").click()		
except:
	#finalizar()
	print("Não foi possível encontrar o vídeo, confira o link fornecido.")
	#os._exit()
sair = 0 #Fecha o app;
while sair != "x":
	print ("Para finalizar aperte x...")
	sair = input()
#finalizar()