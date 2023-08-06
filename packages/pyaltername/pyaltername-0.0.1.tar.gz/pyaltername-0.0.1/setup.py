import setuptools
import pyaltername as palt


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="pyaltername",
    version=palt.__version__,
    author=palt.__author__,
    author_email=palt.__author_email__,
    description="A small python package to name, rename files without conflicts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=palt.__url__,
    packages=setuptools.find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',

    ],
    python_requires='>=3.6',
)
