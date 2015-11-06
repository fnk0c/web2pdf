#!/usr/bin/python
#coding=utf-8

__AUTHOR__	= "Fnkoc"
__DATE__	= "06/11/15"
__LICENCE__	= "GPLV2"

"""
    Copyright (C) 2015  Franco Colombino

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
"""

# ESTE SCRIPT LÊ A LISTA DE ARTIGOS JA PUBLICADOS PELO CIENCIA HACKER E CONVERTE
# O ARTIGO DE HTML PARA PDF. 
# PODE-SE CONVERTER TODOS OS ARTIGOS, OU APENAS UM INTERVALO (3 PRIMEIROS, POR
# EXEMPLO)
#
# ----REQUER PDFKIT, BEAUTIFULSOUP E PYTHON 3----

import pdfkit					#Biblioteca responsavel pela conversao
import urllib.request as u		#Responsalvel por puxar HTML que contem artigos
from bs4 import BeautifulSoup	#Realiza a "filtragem" do HTML (parse html)
from sys import argv			#Le os argumentos

def gen(RANGE, search, downloadURL):
	links = []					#Armazena links

	#Lista de artigos pode ser encontrada no link abaixo
	lista_artigos = "https://github.com/cienciahacker/index/blob/master/Arquivos/Artigos.md"

	html_lista = u.urlopen(lista_artigos)
	html_lista = html_lista.read()
	soup = BeautifulSoup(html_lista, "lxml")

	#Aqui comecamos a parsear o HTML com o beautifulsoup. Abra seu navegador e
	#Clique em inspecionar elementos para entender o que foi feito
	for results in soup.findAll("article", attrs={"class":"markdown-body entry-content"}):
		for link in results.findAll("a", href=True):
			l = link.get("href")
			if "#" in l:	#Nao me lembro mais porque fiz isso e tambem nao me
				pass		#importo mais
			else:
				links.append(l)	#Adiciona links encontrados a lista de links

	if RANGE == False and search == False and downloadURL == False:
		links = links[1:]

	elif RANGE != False and search == False and downloadURL == False:
		links = links[int(RANGE[0]):int(RANGE[1])]  #Range que sera convertido

	elif search != False and RANGE == False and downloadURL == False:
		print(" [!] Searching for: " + search)
		for i in links[1:]:
			if search.replace("\"", "") in i:
				print("[ARTIGO] " + i.replace("http://cienciahacker.com.br/", "").replace("/", "").replace("-", " "))
				print("[URL] " + i + "\n")
			else:
				pass
		exit()

	elif downloadURL != False and RANGE == False and search == False:
		url = downloadURL.split("\"")
		for j in url: 
			url = j

	count = 0	
	total = len(links)
	question = True

	while question == True:
		if downloadURL != False:
			user = input("\n [!] Gerar \"%s\" [Y]es [N]o: " % url.replace("http://cienciahacker.com.br/", "").replace("/", "").replace("-", " ")).lower()
		else:
			user = input("\n [!] Gerar %i PDFs? [Y]es [N]o [S]how: " % total).lower()

		if user == "n":
			print(" [!] Cancelado pelo usuario")
			question = False
			exit()
		elif user == "y":
			print(" [+] Conversao iniciada")
			question = False
		elif user == "s":
			for l in links:
				print(l)
			question = True
	
	if downloadURL != False:
		try:
			out = str(url.replace("http://cienciahacker.com.br/", "").replace("/", "").replace("-", " ") + ".pdf")
			print(" Gerando: %s" % (out))
			pdfkit.from_url(url, out)
			exit()
		except Exception as e:
			pass

		print("\n [+] %s gerado" % out)
		exit()
	else:
		for url in links:
			try:
				out = str(url.replace("http://cienciahacker.com.br/", "").replace("/", "").replace("-", " ") + ".pdf")

				print(" [%i/%i] Gerando: %s" % (count, total, out))
				pdfkit.from_url(url, out)

			except Exception as e:
				pass

			count+=1

	print(" [+] %i PDFs gerados" % count ) 

if __name__ == "__main__":
	if len(argv) <= 1:		#Verifica numero de argumentos
		print("Usage: python web2pdf.py -a -r {start-end} -s \"search term\" -u {url}")
		print("\n [EXEMPLES]\n")
		print("python web2pdf.py -r 1-5")
		print("python web2pdf.py -s \"backdoor\"")
		print("python web2pdf.py -s \"\"")
		print("python web2pdf.py -u \"http://cienciahacker.com.br/beholder/\"")
		print("python web2pdf.py -a")
		
		exit()
	elif len(argv) >= 2:
		if argv[1] == "-a":
			gen(False, False, False)
		elif argv[1] == "-r":
			ran = argv[2].split("-")
			gen(ran, False, False)
		elif argv[1] == "-s":
			keyword = argv[2]
			gen(False, keyword, False)
		elif argv[1] == "-u":
			url = argv[2]
			gen(False, False, url)
		else:
			print("Usage: python web_to_pdf.py -a -r {start-end} -s \"search term\" -u {url}")
			print("\n [EXEMPLES]\n")
			print("python web2pdf.py -r 1-5")
			print("python web2pdf.py -s \"backdoor\"")
			print("python web2pdf.py -s \"\"")
			print("python web2pdf.py -u \"http://cienciahacker.com.br/beholder/\"")
			print("python web2pdf.py -a")
			exit()
