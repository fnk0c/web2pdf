# web2pdf
Gera PDF de todos os artigos do Ciência Hacker presentes na lista de artigos do GitHub

Install
----
* Debian  
  `apt-get install python3 python3-pip wkhtmltopdf`  
  `pip3 install -r requeriments.txt`  
* Arch  
  `pacman -S python python-pip wkhtmltopdf`  
  `pip install -r requeriments.txt`  

Usage
----

```
Usage: python web2pdf.py -a -r {start-end} -s {"search term"} -u {"url"}

 [EXEMPLES]

Download range
 python web2pdf.py -r 1-5

Search for PDF containing "backdoor android"
 python web2pdf.py -s "backdoor android"

Search for all PDFs
 python web2pdf.py -s ""

Download PDF based on URL
 python web2pdf.py -u "https://blog.cienciahacker.ch/beholder/"

Download all PDFs
 python web2pdf.py -a

```
