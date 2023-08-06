import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "JoBase",
    version = "1.1",
    author = "Reuben Grey Ford",
    author_email = "info@jobase.org",
    description = "Python Educational Resource",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "http://jobase.org",
    packages = setuptools.find_packages(),
    install_requires = ['arcade'],    
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)