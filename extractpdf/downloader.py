# -*- coding: utf-8 -*-
import requests

class Downloader:
    """Givne a url to a file, this class downloads it and return
    the path to the saved file.

    Usage:
    dl = Downloader(url, filepath {optional} )

    // to get the saved filename:
    filename = dl.filename

    
    Raises:
        RuntimeError -- [description]
    
    Returns:
        Object -- contains 
    """


    def __init__(self, url, savepath = "", *args, **kwargs):        
        """Initializes the downloader, downloads a file and 
        saves it on the specified location
        
        Arguments:
            url {string} -- a url to a PDF file to download
        
        Keyword Arguments:
            savepath {str} -- optional path location where to download 
            the file to (default: {""} downloads to the local folder)
        """

        super().__init__(*args, **kwargs)

        self.url = url
        self.filename = self.parse_filename(self.url)
        self.full_path = savepath + self.filename

        self.get_pdf()


    @classmethod
    def parse_filename(cls, url):
        if not isinstance(url, str):
            raise AssertionError("argument url must be a string")

        if url.find("/") > 0:
            filename = url.rsplit("/", 1)[1]

        # replaces dotts with dashes, except the last one
        # dotts = url.count(".") - 1
        # filename = filename.replace(".", "-", dotts)
        
        return filename


    def get_pdf(self):
        r = requests.get(self.url, allow_redirects=True, stream=True)
        if r.status_code == 200:
            
            content_length = r.headers.get("content-length", None)
            if int(content_length) > 2e8:
                raise RuntimeError("File size is too large: " + content_length)

            content_type = r.headers.get("content-type", None)
            if content_type != "application/pdf":
                raise RuntimeError("Wrong File type: " + content_type)

            with open(self.full_path, "wb") as fd:
                for chunk in r.iter_content(chunk_size=128):
                    fd.write(chunk)
        else:
            self.last_error = "Download error :: Bad Request"
            raise RuntimeError(self.last_error)
