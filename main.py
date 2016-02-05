# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 18:01:54 2016

@author: pdelboca

References:
===========
 - PyPDF2: https://github.com/mstamy2/PyPDF2

"""
import os.path
from PyPDF2 import PdfFileReader
import csv

_DATA_PATH = os.path.realpath(os.path.dirname(__file__)) + "/data/"


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
    pdf_to_csv()
