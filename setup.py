import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="extractpdf",
    version="0.0.2",

    author="WeAreDevelopers",
    author_email="liad@wearedevelopers.com",
    
    description="A tool to extract text from PDF files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WeAreDevelopers-com/extractpdf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
