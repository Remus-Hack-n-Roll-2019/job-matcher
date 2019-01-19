
import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
import io
from rake_nltk import Rake
import re



def pdfparser(data):

    fp = open(data, 'rb')
    print(dir(fp))
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.

    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data =  retstr.getvalue()

    # # print(data)
    # outfile_name = 'text.txt'
    # with open(outfile_name, 'w') as outfile:
    #     outfile.write(data)

    return data

def extract_keywords(resume_txt):
    regex = re.compile('[a-zA-Z]* [0-9]{4}')

    keywords = []
    lines = resume_txt.split('\n')
    for i, line in enumerate(lines):
        if 'Top Skills' in line:
            keywords.append(lines[i+1])
            keywords.append(lines[i+2])
            keywords.append(lines[i+3])
        if regex.match(line):
            keywords.append(lines[i-1])
        
    return keywords

if __name__ == '__main__':

    data_str = pdfparser('static/Profile.pdf')
    keywords = extract_keywords(data_str)
    print(keywords)







