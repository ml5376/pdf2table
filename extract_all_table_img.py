print('he')

import PyPDF2 
import textract 
print('hi')

"""
* 从PDF中获取某一个章节的内容（写一个函数，第几章由用户确定）。考虑下如果获取子章节
* 从PDF中获取所有表格和图片
* 根据标题定为到某一个表格

"""
# import pdfplumber

# def extract_table():
#     pdf=pdfplumber.open("apreports.pdf")
#     count=len(pdf.pages)
#     for i in range(count):
#         content=pdf.pages[i] # the first table in page 4 , [0] denotes page 1 
#         text=content.extract_text()
#         print(text)
#         # break
        
    
#     return None


# table=extract_table()
# print('table: ',table)

# print(table[0],table[1]) 
import io
# from pdfminer.converter import TextConverter
# from pdfminer.pdfinterp import PDFPageInterpreter
# from pdfminer.pdfinterp import PDFResourceManager
# from pdfminer.pdfpage import PDFPage


# def extract_text_by_page(pdf_path):
#     resource_manager=PDFResourceManager()
#     file_handle=io.StringIO()
#     converter=TextConverter(resource_manager,file_handle)
#     page_interpreter=PDFPageInterpreter(resource_manager,converter)

#     with open(pdf_path, 'rb') as fh:
#         for page in PDFPage.get_pages(fh,caching=True,check_extractable=True):
#             page_interpreter.process_page(page)
#         text=file_handle.getvalue()
    
#     converter.close()
#     file_handle.close()

#     if text:
#         return text
    
# out=extract_text_by_page("apreports.pdf") 
# print(out)
# import PyPDF2

# import tabula 
# dfs=tabula.read_pdf("apreports.pdf",pages='all', multiple_tables=True)
# tables={}
# for i, df in enumerate(dfs):
#         table_name = f"Table {i+1}"
#         first_line=df.iloc[0,:]
#         print(first_line.values)
#         tables[table_name] = df #可以提取表格但也无法提取表格名字
        

# print(dfs)

"""
想要根据标题得到某一个表格
提取位于特定页数的表格
"""
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

            chapter_texts.append(chapter_text)

        return chapter_texts

# Example usage
pdf_file_path = 'example.pdf'
start_page_nums = [1, 10, 20]  # Start page numbers for each chapter
#print text extracted from table in page 2,11,21
start_page_nums=[2,3]

chapter_texts = extract_text_by_chapter(pdf_file_path, start_page_nums)
for i, text in enumerate(chapter_texts, start=1):
    print(f"Chapter {i}:\n{text}\n")       #Bug:提取出来的表格内容不会有空格


def extract_text_from_pdf(pdf_path):
    pdf_file = open(pdf_path, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)

    # 提取文本内容
    text_content = ""
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        text_content += page.extract_text()

    return text_content

# print(extract_text_from_pdf('Online_ticket.pdf'))

from PIL import Image

def extract_images_from_pdf(pdf_path):
    pdf_file = open(pdf_path, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)

    images = []
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        if '/XObject' in page['/Resources']:
            x_object = page['/Resources']['/XObject'].getObject()
            for obj in x_object:
                if x_object[obj]['/Subtype'] == '/Image':
                    image = x_object[obj]
                    images.append(image)

    # 得到图片标注：
    # '图片1': {'/Type': '/XObject', '/Subtype': '/Image', '/Width': 145, '/Height': 100, '/Filter': '/FlateDecode', '/BitsPerComponent': 8, '/ColorSpace': '/DeviceRGB', '/SMask': IndirectObject(5, 0, 4329597488)},

    return images

#得到6张图片，提取文件中所有的表格
import fitz #PyMUPDF
import PIL.Image #pillow 
import io
#extract images from pdf
pdf=fitz.open("Online_ticket.pdf")
counter =1
for i in range(len(pdf)):
    page = pdf[i]
    images=page.get_images()
    for image in images:
        base_img = pdf.extract_image(image[0])
        image_data = base_img["image"]
        img = PIL.Image.open(io.BytesIO(image_data))
        extension=base_img["ext"]
        img.save(open(f"image_{counter}.{extension}", "wb"))
        counter+=1

"""
从文字内容获取表格？
"""
def identify_sections(pdf_path):
    text_content = extract_text_from_pdf(pdf_path)
    images = extract_images_from_pdf(pdf_path)

    # 对文本内容进行标记
    # 这里只是一个示例，你可以根据实际需求来定义标记规则
    # 例如，你可以使用正则表达式来匹配标题、摘要和参考
    sections = {"文字": text_content}

    # 将提取的图片添加到标记中
    for i, image in enumerate(images):
        sections[f"图片{i+1}"] = image
    
    print(sections)

    return sections


identify_sections("Online_ticket.pdf")
