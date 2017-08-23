#!/usr/bin/env python
from __future__ import absolute_import, division, print_function

# Make sure we can import stuff from util/
# This script needs to be run from the root of the DeepSpeech repository
import os
import pandas as pd
import numpy as np
import re
import scipy.io.wavfile as wav
import argparse
import fnmatch

parser = argparse.ArgumentParser(description='Processes and downloads VoxForge dataset.')
parser.add_argument("--wav_dir", default='txt', type=str, help="Directory to store the dataset.")
parser.add_argument("--txt_dir", default='wav', type=str, help="Directory to store the dataset.")
parser.add_argument("--output_file", default='tmp.csv', type=str, help="file path to store the csv.")
args = parser.parse_args()


if __name__ == '__main__':
    wav_dir = args.wav_dir
    txt_dir = args.txt_dir
    output_file = args.output_file
    wav_filenames = os.listdir(wav_dir)
    wav_filenames = [curr_file.split('.')[0] for curr_file in wav_filenames]
    txt_filenames = os.listdir(txt_dir)
    txt_filenames = [curr_file.split('.')[0] for curr_file in txt_filenames]
    filenames = list(set(wav_filenames) & set(txt_filenames))
    print(len(wav_filenames),len(txt_filenames),len(filenames))
    files = []
    for curr_file in filenames:
        files.append((os.path.abspath(os.path.join(wav_dir,curr_file+'.wav')),os.path.abspath(os.path.join(txt_dir,curr_file+'.txt'))))
    df = pd.DataFrame(data=files, columns=["wav_filename", "txt_filename"])
    df.to_csv(output_file,index=False,header=False)
