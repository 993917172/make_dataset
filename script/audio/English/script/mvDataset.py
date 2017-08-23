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
parser.add_argument("--output_wav_dir", default='output', type=str, help="Directory to store the dataset.")
parser.add_argument("--output_txt_dir", default='output', type=str, help="Directory to store the dataset.")
args = parser.parse_args()


if __name__ == '__main__':
    wav_dir = args.wav_dir
    txt_dir = args.txt_dir
    output_wav_dir = args.output_wav_dir
    output_txt_dir = args.output_txt_dir
    if not os.path.isdir(output_wav_dir):
        os.makedirs(output_wav_dir)
    if not os.path.isdir(output_txt_dir):
        os.makedirs(output_txt_dir)
    for root, root_dir_names, root_file_names in os.walk(wav_dir):
        for filename in fnmatch.filter(root_file_names, '*.wav'):
            os.system("mv "+os.path.join(root, filename)+' '+os.path.join(output_wav_dir, filename))
    print("move wav finished")
    for root, root_dir_names, root_file_names in os.walk(txt_dir):
        for filename in fnmatch.filter(root_file_names, '*.txt'):
            os.system("mv "+os.path.join(root, filename)+' '+os.path.join(output_txt_dir, filename))
    print("move txt finished")
