from setuptools import setup, find_packages

setup(
    name="stock-evaluator",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'yfinance',
        'pandas'
    ],
    python_requires='>=3.7',
) 
