import os
import shutil
import six
from tempfile import mkdtemp

from .exceptions import UnknownMethod, ShellError

from .shell_parser import ShellParser
from .image import Parser as TesseractParser


class Parser(ShellParser):
    """Extract text from pdf files using either the ``pdftotext`` method
    (default) or the ``pdfminer`` method as a fallback.
    """

    def extract(self, filename, method='', **kwargs):
        if method == '' or method == 'pdftotext':
            try:
                return self.extract_pdftotext(filename, **kwargs)
            except ShellError as ex:
                # If pdftotext isn't installed and the pdftotext method
                # wasn't specified, then gracefully fallback to using
                # pdfminer instead.
                if method == '':
                    return self.extract_pdfminer(filename, **kwargs)
                else:
                    raise ex
        elif method == 'pdfminer':
            return self.extract_pdfminer(filename, **kwargs)
        elif method == 'tesseract':
            return self.extract_tesseract(filename, **kwargs)
        else:
            raise UnknownMethod(method)

    def extract_pdftotext(self, filename, **kwargs):
        """Extract text from pdfs using the pdftotext command line utility."""
        if 'layout' in kwargs:
            args = ['pdftotext', '-layout', filename, '-']
        else:
            args = ['pdftotext', filename, '-']
        stdout, _ = self.run(args)
        return stdout

    def extract_pdfminer(self, filename, **kwargs):
        """Extract text from pdfs using pdfminer."""

        pdf2txt_path = self.find('pdf2txt.py', '/')

        stdout, _ = self.run(['python', pdf2txt_path, filename])
        return stdout

    def extract_tesseract(self, filename, **kwargs):
        """Extract text from pdfs using tesseract (per-page OCR)."""
        temp_dir = mkdtemp()
        base = os.path.join(temp_dir, 'conv')
        contents = []
        try:
            self.run(['pdftoppm', filename, base])

            for page in sorted(os.listdir(temp_dir)):
                page_path = os.path.join(temp_dir, page)
                page_content = TesseractParser().extract(page_path, **kwargs)
                contents.append(page_content)
            return six.b('').join(contents)
        finally:
            shutil.rmtree(temp_dir)
    
    @classmethod
    def find(cls, name, path):
        """Finds a file by its name in the system
        
        Arguments:
            name {str} -- file name to search
            path {str} -- a starting path to search from
        
        Returns:
            str -- the path location of the file
        """

        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)
