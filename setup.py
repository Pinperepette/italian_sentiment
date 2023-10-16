#!/usr/bin/env python

from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess

class CustomInstallCommand(install):
    def run(self):
        subprocess.run(['python', '-m', 'spacy', 'download', 'it_core_news_sm'])
        install.run(self)

setup(
    name='italian_sentiment',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'spacy==3.7.1',
        'numpy==1.26.1',
        'keras==2.14.0',
        'tensorflow==2.14.0'
    ],
    entry_points={
        'console_scripts': [
            'nome-comando=italian_sentiment.script:funzione_principale',
        ],
    },
    include_package_data=True,
    package_data={
        'italian_sentiment': ['files/*.pkl', 'files/*.h5'],
    },
    author='Pinperepette',
    author_email='pinperepette@gmail.com',
    description='Un pacchetto per l\'analisi del sentiment in italiano',
    url='https://link-al-tuo-repository',
    license='MIT License',
    cmdclass={'install': CustomInstallCommand}
)