# extractpdf
A python package focused on extracting content out of PDF files.

There seems to be [many options out there](https://stackoverflow.com/questions/34837707/how-to-extract-text-from-a-pdf-file), but no single solution that is easy to install, even on Windows, and focus specifically on PDF files. So we have created this extractpdf package.

It is based on [Textract](https://github.com/deanmalmgren/textract) structure, but focuses on PDF only, and adds also other tools to the pipline, such as [PyPDF2](https://pythonhosted.org/PyPDF2/) and [Camelot](https://camelot-py.readthedocs.io/en/master/).


# Usage:
To use this package, install it from pypi using:
```
pip install extractpdf
```

Then use it like so:
```python
import extractpdf as epdf

# local file
content = epdf.process('my_file.pdf')
# url:
content = epdf.process('http://www.example.com/some_file.pdf')
```

# Advanced Usage:
To control more features, one can use the PDFExtractor itself:
```python
from extractpdf import PDFExtractor
epdf = PDFExtractor()
content = epdf.get_content('http://www.example.com/some_file.pdf', keep_download=True)
f = epdf.filename # f = some_file.pdf
epdf.delete_file()
```

# Development
We welcome contributers warmly!

For running this project locally, you need first to install the dependency packages.
To install them, you can use [pipenv](https://docs.pipenv.org/):

#### Installation using pipenv (which combines virtualenv with pip)

Install pipenv

```bash
# if you haven't installed pip
sudo easy_install pip

# install pipenv
pip install pipenv
```

On MacOS - you can use homebrew:
```
brew install pipenv
```

Set the pipenv to be local in the project:
On Windows:
```bash
set PIPENV_VENV_IN_PROJECT=true 
```

On Mac/Linux:
```bash
export PIPENV_VENV_IN_PROJECT=true 
```

... and then, install the packages and run the server
```
 # install all packages
pipenv install
```

