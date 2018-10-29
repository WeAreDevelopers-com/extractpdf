from .pdf_extractor import PDFExtractor

name = "extractpdf"
VERSION = "0.0.2"

def process(pdf_path):
    """This is the main function of extractpdf.
    It recieve a pdf_path as a local file path or a URL to a pdf file online.
    
    Arguments:
        pdf_path {str} -- can be either a local file or a URL
    """
    pe = PDFExtractor()
    return pe.get_content(pdf_path)
