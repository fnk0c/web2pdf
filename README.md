# web2pdf
--------
Gera PDF de todos os artigos do Ciência Hacker presentes na lista de artigos do GitHub

### Installing Dependencies
--------

**Debian**  

    sudo apt-get install python3, python3-pip  

**Arch**  

    sudo pacman -S python python-pip  

**After that**  

    pip3 install -r requeriments.txt  

### Help 
--------

    Usage: python web_to_pdf.py -a -r {start-end} -s {"search term"} -u {"url"}
     
      [EXEMPLES]
      
    python web2pdf.py -r 1-5
    python web2pdf.py -s "backdoor"
    python web2pdf.py -s ""
    python web2pdf.py -u "http://cienciahacker.com.br/beholder/"
    python web2pdf.py -a

### Using
--------

Download all PDFs

    python web2pdf.py -a

Search for PDFs

    python web2pdf.py -s "backdoor"

List all PDFs

    python web2pdf.py -s ""

Download range of PDFs

    python web2pdf.py -r 1-5

Download PDF of URL

    python web2pdf.py -u "http://cienciahacker.com.br/beholder/"
