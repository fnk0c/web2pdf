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
# ----REQUER PDFKIT, BEAUTIFULSOUP, LXML E PYTHON 3----

import pdfkit					#Biblioteca responsavel pela conversao
try:
	import urllib.request as u	#Responsalvel por puxar HTML que contem artigos
except:
	import urllib as u
from bs4 import BeautifulSoup	#Realiza a "filtragem" do HTML (parse html)
from sys import argv, path
from os import system
path.append("configuration")
from config import *

def main(RANGE, search, downloadURL):
	"""
	REALIZA PARSE DO HTML E CONVERSAO PARA PDF  ################################
	"""
	def gerador(URL, OUT):
		content = []

		html = u.urlopen(URL)
		soup = BeautifulSoup(html.read().decode("utf-8"), "lxml")

		for i in soup.findAll("article"):#, attrs={"class":"entry-content"}):
			content.append(i)

		src = \
"""\
<html lang=pt-BR>
<head><style>footer{display:none;}.comment{display:none;} </style><meta charset="utf-8"></head><body bgcolor="#FFFFFF">
%s
</html>
""" % str(content).replace("[", "").replace("]", "")

		with open("out.html", "w") as output:
			output.write(src)
		pdfkit.from_file("out.html", "output/%s" % OUT, options=options, css=css)

	"""
	COLETA TODOS OS LINKS DO GITHUB  ###########################################
	"""
	links = []					#Armazena links
	
	if downloadURL != False:
		skip = True
	else:
		skip = False

	if skip == False:

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
	else:
		print("pulando")

	"""
	REALIZA FILTRO DAS URLS  ###################################################
	"""

	#adiciona todos os artigos
	if RANGE == False and search == False and downloadURL == False:
		links = links[1:]

	#adiciona apenas range de artigos
	elif RANGE != False and search == False and downloadURL == False:
		links = links[int(RANGE[0]):int(RANGE[1])]  #Range que sera convertido

	#procura por artigos
	elif search != False and RANGE == False and downloadURL == False:
		print(" [!] Searching for: " + search)
		for i in links[1:]:
			for j in search.split(" "):
				if j.replace("\"", "") in i:
					print("[ARTIGO] " + i.replace("http://cienciahacker.com.br/", "").replace("/", "").replace("-", " "))
					print("[URL] " + i + "\n")
				else:
					pass
		exit()

	#adiciona apenas artigo especificado
	elif downloadURL != False and RANGE == False and search == False:
		url = downloadURL.split("\"")
		for j in url: 
			url = j

	"""
	PEDE PARA USUÁRIO CONFIRMAR A AÇÃO  ########################################
	"""

	count = 0	
	total = len(links)
	question = True

	while question == True:
		#pede confirmacao do usuario
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

	"""
	REALIZA FILA PARA CONVERSÃO DO HTML EM PDF  ################################
	"""

	#converte apenas uma url
	if downloadURL != False:
		try:
			out = str(url.replace("http://cienciahacker.com.br/", "").replace("/", "").replace("-", " ") + ".pdf")
			print(" Gerando: %s" % (out))
			gerador(url, out)

		except Exception as e:
			pass
			print(e)

		print("\n [+] %s gerado" % out)
		system("rm -rf out.html")
		exit()

	#converte lista de urls
	else:
		for url in links:
			try:
				out = str(url.replace("http://cienciahacker.com.br/", "").replace("/", "").replace("-", " ") + ".pdf")
				print(" [%i/%i] Gerando: %s" % (count, total, out))
				gerador(url, out)

			except Exception as e:
				pass
				print(e)

			count+=1

	print(" [+] %i PDFs gerados" % count )
	system("rm -rf out.html")

if __name__ == "__main__":

	help = """
Usage: python web2pdf.py -a -r {start-end} -s {"search term"} -u {"url"}

 [EXEMPLES]

Download range
 python web2pdf.py -r 1-5

Search for PDF containing "backdoor android"
 python web2pdf.py -s "backdoor android"

Search for all PDFs
 python web2pdf.py -s ""

Download PDF based on URL
 python web2pdf.py -u "http://cienciahacker.com.br/beholder/"

Download all PDFs
 python web2pdf.py -a
"""

	#Verifica numero de argumentos
	if len(argv) <= 1:
		print(help)
		exit()
	elif len(argv) >= 2:
		#Todos os artigos
		if argv[1] == "-a":
			main(False, False, False)
		#Range de artigos
		elif argv[1] == "-r":
			ran = argv[2].split("-")
			main(ran, False, False)
		#Busca por artigos
		elif argv[1] == "-s":
			keyword = argv[2]
			main(False, keyword, False)
		#Usa url do artigo
		elif argv[1] == "-u":
			url = argv[2]
			main(False, False, url)
		else:
			print(help)
			exit()
