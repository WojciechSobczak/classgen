from setuptools import setup

setup(
    name='classgen',
    version='0.0.0',    
    description='Python package for classes generation from python source templates',
    url='https://github.com/WojciechSobczak/classgen',
    author='Wojciech Sobczak',
    author_email='',
    license='Apache 2.0',
    packages=['classgen', 'classgen.cpp'],
    install_requires=['jinja2'],
    classifiers=['Programming Language :: Python :: 3.11',],
    include_package_data=True
)
