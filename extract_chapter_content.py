import PyPDF2

"""
根据章节/子章节名字的字符串提取文件内容，内容提取的范围精确到页（不是很精确）
首先需要根据pdf2c.py提取章节名字和他们的开始页并把结果写入.txt file 
process txt file to get respective page number for retrieving information
"""
def get_page_by_chap(dict,chap_name):
    from_page=0
    till_page=0
    for i in range(len(dict['title'])):
        if dict['title'][i]==chap_name:
            from_page=dict['page'][i]
            # till_page=dict   
  

def locate_chapter_by_chapter_name():
    dict={}
    dict['page']=[]
    dict['title']=[]
    with open('outline.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line != '\n':
                info=line.split(' ')
                print(info)
                str=''
                for i in range(len(info)-1):
                    if i is not 0:
                        str+=info[i]
                # print(str) 
            
                # print(len(info))
                dict['title'].append(str.replace('\t',''))
                dict['page'].append(info[0])
                
    return dict
def find_start_end_page(dict,chap_name): #chapter and sub-chapter have equal importance
    start=0
    end=0
    for i in range(len(dict['title'])):
        if str(dict['title'][i]) == str(chap_name):
            print(dict['title'][i])
            start=dict['page'][i]
            end=dict['page'][i+1]
    # print(start,end)
    if start==end==0:
        print('no valide (sub)chapter can be found')
        return 0
    return [i for i in range(int(start),int(end)+1)]#[inclusive,inclusive]

def find_text_by_page_nums(pdf_file, page_nums):
    fileobj=open(pdf_file,'rb')
    pdfReader = PyPDF2.PdfFileReader(fileobj)
    for i in page_nums:
        pageObj = pdfReader.getPage(i-1)
        text = pageObj.extractText().split("  ")
        for i in range(len(text)):
            print(text[i],end="\n\n")


dict=locate_chapter_by_chapter_name()
print(dict)
print(find_start_end_page(dict, "5.经营效率"))

page_nums =find_start_end_page(dict, "5.经营效率")
print(find_text_by_page_nums("example.pdf",page_nums))