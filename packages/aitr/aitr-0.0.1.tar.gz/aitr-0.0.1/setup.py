from distutils.core import setup
import setuptools

setup(
    name="aitr",
    version="0.0.1",
    packages=['aitr'],
    description="Artificial Intelligence for Turkish",
    long_description=open('README.md', encoding="utf8").read(),
    long_description_content_type='text/markdown',
    url="https://github.com/msaidzengin/aitr",
    author="M. Said Zengin",
    author_email="msaidzengin@gmail.com",
    maintainer="M. Said Zengin",
    maintainer_email="msaidzengin@gmail.com",
    keywords=['ai', 'turkish', 'tur', 'artificial intelligence', 'yapay zeka', 'makine ögrenmesi'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
