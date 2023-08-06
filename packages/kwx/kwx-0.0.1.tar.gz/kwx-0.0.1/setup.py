try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from setuptools import find_namespace_packages
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setup_args = dict(
    name="kwx",
    version="0.0.1",
    author="Andrew Tavis McAllister",
    author_email="andrew.t.mcallister@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    description="Unsupervised keyword extraction in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_namespace_packages(),
    license="new BSD",
    url="https://github.com/andrewtavis/kwx",
)

on_rtd = os.environ.get("READTHEDOCS") == "True"
if on_rtd:
    install_requires = []
else:
    install_requires = [
        "numpy",
        "xlrd",
        "pandas",
        "matplotlib",
        "mpl_toolkits",
        "seaborn",
        "stopwordsiso",
        "gensim",
        "pyLDAvis",
        "wordcloud",
        "nltk",
        "spacy",
        "emoji",
        "googletrans",
        "scikit-learn",
        "keras",
        "IPython",
        "sentence-transformers",
        "tqdm",
    ]

if __name__ == "__main__":
    setup(**setup_args, install_requires=install_requires)
