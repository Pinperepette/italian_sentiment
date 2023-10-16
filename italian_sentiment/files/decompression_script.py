#!/usr/bin/env python
import os
import lzma
import shutil


script_dir = os.path.dirname(os.path.abspath(__file__))
num_chunks = 10

merged_file_path = os.path.join(script_dir, 'merged_chunks.xz')
with lzma.open(merged_file_path, 'wb') as f_out:
    for i in range(num_chunks):
        chunk_file = os.path.join(script_dir, f'output_chunk_{i}.xz')
        with lzma.open(chunk_file, 'rb') as f_in:
            shutil.copyfileobj(f_in, f_out)

decompressed_file_path = os.path.join(script_dir, 'model_lstm.h5')
with lzma.open(merged_file_path, 'rb') as compressed_file:
    with open(decompressed_file_path, 'wb') as decompressed_file:
        shutil.copyfileobj(compressed_file, decompressed_file)

if os.path.exists(decompressed_file_path):
    print(f"File '{decompressed_file_path}' creato con successo.")
else:
    print("Errore durante la creazione del file.")