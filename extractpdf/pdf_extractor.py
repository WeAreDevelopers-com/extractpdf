# -*- coding: utf-8 -*-
import datetime
import requests
import logging
import os
from urllib.parse import urlparse
from .parser import Parser
from .downloader import Downloader

logger = logging.getLogger(__name__)

class PDFExtractor(object):
    """
    PDFExtractor is the main part of the package. 
    It recieves a string representing a URL or a local PDF file, downloads the file if needed,
    extracts and returns its content as a string.
    """

    def __init__(self, path=""):
        """initializes the PDF Extractor object with an optional path
        where to download the files to process when it comes from a URL
        
        Keyword Arguments:
            path {str} -- A default path to save downloaded files to (default: {""})
        """

        self.initTime = datetime.datetime.now().timestamp()
        
        if path == "":
            self.path = os.getcwd()
        else:
            self.path = path

    @classmethod
    def is_url(cls, url):
        """Simple method to determine if the given string is a url or a 
        local file path
        
        Arguments:
            url {string} -- a path url to a file with a scheme
        
        Returns:
            bool -- true if the given URL is external internet URL
        """
        return urlparse(url).scheme in ('http', 'https',)

    def download_file(self, url):
        """If a url was given, download the file from the internet, 
        and save the filename internally

        TODO: set the downloader to download a temporary file,
        such as ShellParser.temp_filename()

        Arguments:
            url {string} -- A url for a file to download
        
        Returns:
            string -- pdf filename or empty string if an error occured
        """
        try:
            dl = Downloader(url)
        except RuntimeError:
            return ""

        return dl.full_path

    def parse_pdf(self):
        if not (self.full_filename):
            raise AssertionError("PDF filename must not be empty")

        parser = Parser()
        self.pdf_content = parser.process(self.full_filename, encoding="utf-8")

    def delete_file(self):
        if not (self.full_filename):
            raise AssertionError("PDF filename must not be empty")

        if os.path.exists(self.full_filename):
            os.remove(self.full_filename)

    def get_content(self, url="", keep_download = False):
        if not isinstance(url, str):
            raise AssertionError("argument url must be a string")

        if not (url and url.strip()):
            raise AssertionError("argument url must not be empty")

        isurl = self.is_url(url)

        self.full_filename = self.download_file(url) if isurl else url
        self.filename = Downloader.parse_filename(self.full_filename)

        self.parse_pdf()

        if isurl and not keep_download:
            self.delete_file()

        return self.pdf_content

    def __exit__(self, exception_type, exception_value, traceback):
        self.endTime = datetime.datetime.now().timestamp()
        logger.info(self.initTime - self.endTime)
