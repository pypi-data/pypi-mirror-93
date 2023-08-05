"""
Created on Wen Apr 8 10:18 2020

@author: Hanwen Xu

E-mail: hw-xu16@mails.tsinghua.edu.cn

New update: process data with unknown content
"""
from setuptools import setup, find_packages

setup(
    name="RareDecipher",
    version="0.1.0",
    keywords=("pip", "RareDecipher"),
    description="RareDecipher: Robust and accurate inference of rare cell type proportions from bulk gene expression or DNA methylation data",
    long_description="RareDecipher: Robust and accurate inference of rare cell type proportions from bulk gene expression or DNA methylation data",
    license="Hanwen",

    url="https://github.com/WangLabTHU/RareDecipher/",
    author="Hanwen Xu",
    author_email="xuhw20@mails.tsinghua.edu.cn",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['numpy', 'tqdm', 'scipy', 'sklearn', 'statsmodels', 'pandas']
)