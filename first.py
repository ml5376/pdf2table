
import re
import requests

import pdfplumber
import pandas as pd
from collections import namedtuple

def download_file(url):
    local_filename = url.split('/')[-1]
    
    with requests.get(url) as r:
        with open(local_filename, 'wb') as f:
            f.write(r.content)
        
    return local_filename


ap_url = 'https://www.tabs3.com/support/sample/apreports.pdf'
ap = download_file(ap_url)

with pdfplumber.open(ap) as pdf:
    page = pdf.pages[15]
    pdf_text = page.extract_text()
    
# print(pdf_text)
# print(text)
from pdfminer.high_level import extract_pages, extract_text

text=extract_text("apreports.pdf")
# print(text)

for page_layout in extract_pages("apreports.pdf"):
    for element in page_layout:
        # print(element)
        break


# print(text)

pattern=re.compile(r"[a-zA-Z]+,{1}\s{1}")
matche=pattern.findall(text)
# print(matche)

import fitz #PyMUPDF
import PIL.Image #pillow 
import io

pdf=fitz.open("example.pdf")#extract images from pdf
counter =1
for i in range(len(pdf)):
    page = pdf[i]
    images=page.get_images()
    for image in images:
        base_img = pdf.extract_image(image[0])
        image_data = base_img["image"]
        img = PIL.Image.open(io.BytesIO(image_data))
        extension=base_img["ext"]
        img.save(open(f"image{counter}.{extension}", "wb"))
        counter+=1

#extract table from pdf 
import tabula 
dfs=tabula.read_pdf("apreports.pdf",pages='all', multiple_tables=True)
tables={}
for i, df in enumerate(dfs):
        table_name = f"Table {i+1}"
        first_line=df.iloc[0,:]
        print(first_line.values)
        tables[table_name] = df
        

# print(tables)




    