# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 18:01:54 2016

@author: pdelboca

References:
===========
 - PyPDF2: https://github.com/mstamy2/PyPDF2

"""
import os.path
import sys
from PyPDF2 import PdfFileReader
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import re
import progressbar

_DATA_PATH = os.path.realpath(os.path.dirname(__file__)) + "/data/"
_PDF_PATH = _DATA_PATH + "pdfs/"
_TXT_BOLETINES_PATH = _DATA_PATH + "urls_boletin.txt"

def scrapear_url_boletines():
    """
    Scrapea iterativamente todos los links a los pdfs de los boletines de
    la pagina:
        - http://boletinoficial.cba.gov.ar/{year}/{month}/
    Nota:
        - El metodo junta todos los links y los exporta a un txt para luego ser
        usados. Esto no es necesario, pero queria tener una lista de links
        para compartir.
        - Scrapea los links a los pdf encontrados en la página, en la práctica 
        son solo boletines oficiales. Pero la logica no hace chequeo alguno de 
        que realmente sean. Si hay otros archivos en pdf, tambien los descarga.
    """
    pdf_links = []
    for year in range(2007,2017):
        print("Scrapeando links del {0}".format(year))        
        for month in range(1,13):
            url = "http://boletinoficial.cba.gov.ar/{0}/{1}/".format(year, str(month).zfill(2))
            req = Request(url)
            try:
                response = urlopen(req)
            except HTTPError as e:
                print('Error en la url: {0}'.format(url))
                print(e.code, " - ", e.reason)
            except URLError as e:
                print('Error en la url: {0}'.format(url))
                print(e.code, " - ", e.reason)
            else:
                html = response.read()
                links = re.findall('"(http:\/\/.*?)"', str(html))
                pdf_links.extend([link for link in links if link.endswith('.pdf')])
    print("Links obtenidos, comenzando la escritura a archivo...")
    with open(_TXT_BOLETINES_PATH, "w") as urls_file:
        for link in pdf_links:
            urls_file.write("%s\n" % link)
    print("Escritura finalizada.")


def descargar_boletines():
    """
    Descarga iterativamente todos los pdf de la pagina:
        - http://boletinoficial.cba.gov.ar/{year}/{month}/
    Nota:
        - Utiliza los links obtenidos en el método scrapear_url_boletines
    """    
    if not os.path.isfile(_TXT_BOLETINES_PATH):
        print("No existe el archivo: {0}".format(_TXT_BOLETINES_PATH))
        print("Ejecute el metodo scrapear_url_boletines para obtener las url.")
    else:
        print("Comenzando la descarga de Boletines")
        with open(_TXT_BOLETINES_PATH, 'r') as url_boletines:
            urls = url_boletines.read().splitlines()
        bar = progressbar.ProgressBar()
        for url in bar(urls):
            filename = url.split("/")[-1]
            file_path = _PDF_PATH + filename
            req = Request(url)
            try:
                pdf_file = urlopen(req)
            except HTTPError as e:
                print('Error en la url: {0}'.format(url))
                print(e.code, " - ", e.reason)
            except URLError as e:
                print('Error en la url: {0}'.format(url))
                print(e.code, " - ", e.reason)
            else:
                with open(file_path, 'wb') as local_file:
                    local_file.write(pdf_file.read())
    print("Descarga Finalizada")
    

def pdf_to_csv():
    """
    Iterates throught all the pdf stored in ./data/pdf/ folder and export its 
    content to the file data.csv.
    The format of the csv file should have two columns: id and text
    """
    pdf_data_path = _DATA_PATH + "pdf/"   
    csv_data_file = _DATA_PATH + "data.csv"
    with open(csv_data_file, "w", newline='') as csvfile:        
        data_writer = csv.writer(csvfile)
        data_writer.writerow(["id","texto"])        
        for fn in os.listdir(pdf_data_path):
            file_path = os.path.join(pdf_data_path, fn)         
            if file_path.endswith(".pdf"):
                input_file = PdfFileReader(open(file_path, 'rb'))
                text = ""
                for p in range(input_file.getNumPages()):
                    text += input_file.getPage(p).extractText() + " "
                data_writer.writerow([fn,text])
        

if __name__ == "__main__":
    #pdf_to_csv()
    #scrapear_url_boletines()    
    descargar_boletines()
