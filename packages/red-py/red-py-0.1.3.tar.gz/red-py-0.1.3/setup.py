from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='red-py',
    version='0.1.3',
    description='A library of useful tools and extensions',
    url='https://github.com/zhooda/red-py.git',
    author='Zeeshan Hooda',
    author_email='zhooda@protonmail.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Education',
        'Programming Language :: Python :: 3.6',        
        'Programming Language :: Python :: 3.7',        
        'Programming Language :: Python :: 3.8',        
        'Programming Language :: Python :: 3.9',        
    ],
)
