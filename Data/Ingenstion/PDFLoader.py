from .Base import DocumentLoader
# pyrefly: ignore [missing-import]
from pypdf import pdfReader
from .Document import Document

class PDFLoader (DocumentLoader):
    def __init__(self,path):
        self.path=path
    def load(self):
        reader=pdfReader(self.path)
        pages=[]
        for page_num,page in enumerate(reader.pages,start=1):
            text=page.extract_text()
            if text :
                pages.append(Document(content=text,meta_data={
                    "Source":self.path,
                    "Page_Number":page_num 
                }))
                return pages
            else:
                raise ValueError("This type file is not supported")

