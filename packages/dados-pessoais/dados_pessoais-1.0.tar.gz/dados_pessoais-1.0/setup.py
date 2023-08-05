from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='dados_pessoais',
    version=1.0,
    description='Este pacote irá fornecer ferramentas para armazenamento de dados pessoais',
    long_description=Path('README.md').read_text(),
    author='Gustavo Nogueira',
    author_email='gustavonogueiralopes@gmail.com',
    keywords=['dados pessoais', 'nascimento', 'informações'],
    packages=find_packages()
)
