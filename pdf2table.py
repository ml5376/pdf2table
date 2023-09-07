import pdfplumber 

def extract_table():
    pdf=pdfplumber.open("apreports.pdf")
    count=len(pdf.pages)
    for i in range(count):
        content=pdf.pages[i] # the first table in page 4 , [0] denotes page 1 
        text=content.extract_text()
        print(text)
        break
        
    table=content.extract_table()
    
    return table 

# table=extract_table()

# print(table[0],table[1]) 
import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage


def extract_text_by_page(pdf_path):
    resource_manager=PDFResourceManager()
    file_handle=io.StringIO()
    converter=TextConverter(resource_manager,file_handle)
    page_interpreter=PDFPageInterpreter(resource_manager,converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,caching=True,check_extractable=True):
            page_interpreter.process_page(page)
        text=file_handle.getvalue()
    
    converter.close()
    file_handle.close()

    if text:
        return text
    
out=extract_text_by_page("apreports.pdf") 
# print(out)
# import PyPDF2

import PyPDF2
def extract_text_by_chapter(pdf_file_path, start_page_nums):
    with open(pdf_file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        total_pages = pdf_reader.numPages

        chapter_texts = []
        for start_page in start_page_nums:
            if start_page > total_pages:
                print(f"Invalid start page: {start_page}. Skipping.")
                continue

            chapter_text = ''
            end_page = start_page + 1 if start_page + 1 < total_pages else total_pages
            for page_num in range(start_page, end_page):
                page = pdf_reader.getPage(page_num)
                chapter_text += page.extract_text()

            chapter_texts.append(chapter_text.strip())

        return chapter_texts

# Example usage
pdf_file_path = 'apreports.pdf'
start_page_nums = [1, 10, 20]  # Start page numbers for each chapter

chapter_texts = extract_text_by_chapter(pdf_file_path, start_page_nums)
for i, text in enumerate(chapter_texts, start=1):
    print(f"Chapter {i}:\n{text}\n")         