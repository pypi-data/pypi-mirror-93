from setuptools import setup
__project__ = "numtostring"
__version__ = "0.1.1"
__description__ = "A simple int-to-string converter to covert numbers like 10 to strings like ten"
__packages__ = ["numtostring"]
__author__ = "khhs"
__author_email__ = "khhs1671@gmail.com"
__url__ = "https://github.com/Khhs167/number-to-string/"
__keywords__ = ["number to text", "conversion"]

__classifiers__ = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Other Audience",
    "Programming Language :: Python :: 3",
]

setup(
    name = __project__,
    version = __version__,
    description = __description__,
    packages = __packages__,
    author = __author__,
    author_email = __author_email__,
    url = __url__,
    classifiers = __classifiers__,
    keywords = __keywords__,
    long_description='''# numtostring
    Numtostring(or numbertostring, as the import name is) is a tool for converting numbers/ints like 10 to pieces of text like ten!
    ## Example of usage
    ```py
    import numbertostring as numtostring
    print(numtostring.convert(245))
    # Output: two hundred and forty five
    ```''',
    long_description_content_type='text/markdown',
)