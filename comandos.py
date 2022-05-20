# -*- coding: utf-8 -*-
from logging import error
import sys #coleta o link
import time #tempo de espera da url
from urllib import request, parse
from warnings import catch_warnings #biblioteca da url
from selenium import webdriver #Coleta o nome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from datetime import datetime #define a hora
import os #comando para o shell

def finalizar():
	driver.close()
	driver.quit()
	return None

for arg in sys.argv:
	print(arg)
print ("Buscando vídeo")

#Coleta dados do browser

options = Options()
options.add_argument('--headless')
options.add_argument('window-size=800x600') # optional
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
#acessando dados
try:
	driver.get(arg)
	nome = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text	
	print (nome)
	sair = 0
	while sair != "x":
		print ("Para finalizar aperte x...")
		sair = input()
except:
	finalizar()
	print("Não foi possível encontrar o vídeo, confira o link fornecido.")
	os._exit()

finalizar()