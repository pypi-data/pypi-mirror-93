from distutils.core import setup
import setuptools

setup(
    name="nlptur",
    version="0.0.1",
    packages=['nlptur'],
    description="Natural language processing tool for Turkish",
    long_description=open('README.md', encoding="utf8").read(),
    long_description_content_type='text/markdown',
    url="https://github.com/msaidzengin/nlptur",
    author="M. Said Zengin",
    author_email="msaidzengin@gmail.com",
    maintainer="M. Said Zengin",
    maintainer_email="msaidzengin@gmail.com",
    keywords=['nlp', 'turkishnlp', 'python', 'natural language processing', 'language processing', 'dogal dil isleme'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
