from Data.Ingenstion.PDFLoader import PDFLoader
from Data.Ingenstion.TextLoader import TextLoader







class LoaderFactory :
    @staticmethod
    def create(file_path):
        if file_path.endswith(".txt"):
            return TextLoader
        elif file_path.endswith(".pdf"):
            return PDFLoader