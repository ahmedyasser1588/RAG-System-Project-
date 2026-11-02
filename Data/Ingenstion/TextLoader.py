from .Base import DocumentLoader 
from .Document import Document
#load File and return Meta Data and Content
class TextLoader(DocumentLoader):
     def __init__(self,file_path):
        self.file_path=file_path
    
     def load(self):
        with open(self.file_path,"r",encoding="utf-8") as f:
            content=f.read()
            return (Document(
                content=content,
                meta_data={
                    "source":self.file_path,
                    "File_Type":"txt",
                    "author":None,}
            )
            )



