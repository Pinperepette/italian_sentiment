#!/usr/bin/env python

from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import subprocess
import lzma
import shutil

class CustomInstallCommand(install):
    def run(self):
        subprocess.run(['python', '-m', 'spacy', 'download', 'it_core_news_sm'])
        install.run(self)
        model_weights_path = os.path.join(self.install_lib, 'italian_sentiment', 'files', 'model_lstm.h5')
        if not os.path.exists(model_weights_path):
            print("File 'model_lstm.h5' not found. Generating model weights...")
            self.combine_chunks_and_create_model(model_weights_path)

    def combine_chunks_and_create_model(self, model_weights_path):
        chunk_files = ['output_chunk_0.xz', 'output_chunk_1.xz', 'output_chunk_2.xz',
                       'output_chunk_3.xz', 'output_chunk_4.xz', 'output_chunk_5.xz',
                       'output_chunk_6.xz', 'output_chunk_7.xz', 'output_chunk_8.xz', 'output_chunk_9.xz']

        # Esegui lo script di decompressione nella cartella appropriata
        decompression_script_path = os.path.join(self.install_lib, 'italian_sentiment', 'files', 'decompression_script.py')
        subprocess.run(['python', decompression_script_path])

        # Verifica se il file 'model_lstm.h5' è stato creato correttamente
        if os.path.exists(model_weights_path):
            print("Model weights created successfully.")
        else:
            print("Errore durante la creazione del file.")

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
            'italian_sentiment-install=italian_sentiment.script:funzione_principale',
        ],
    },
    include_package_data=True,
    package_data={
        'italian_sentiment': ['files/*']
    },
    author='Pinperepette',
    author_email='pinperepette@gmail.com',
    description='Un pacchetto per l\'analisi del sentiment in italiano',
    url='https://github.com/Pinperepette/italian_sentiment/',
    license='MIT License',
    cmdclass={'install': CustomInstallCommand}
)
