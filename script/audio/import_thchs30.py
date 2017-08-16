#!/usr/bin/env python
from __future__ import absolute_import, division, print_function

# Make sure we can import stuff from util/
# This script needs to be run from the root of the DeepSpeech repository
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import codecs
import fnmatch
import pandas
import progressbar
import subprocess
import tarfile
import unicodedata
import json
from utils import update_progress
from sox import Transformer
from tensorflow.contrib.learn.python.learn.datasets import base
from tensorflow.python.platform import gfile

def _preprocess_data(data_dir):

    print("Converting trn and splitting transcriptions...")
    work_dir = data_dir
    phone_set = set()
    train_df, phone_set = _convert_audio_and_split_sentences(work_dir, "train", "train-wav", "train-txt", phone_set)
    dev_df, phone_set = _convert_audio_and_split_sentences(work_dir, "dev", "dev-wav", "dev-txt", phone_set)
    test_df, phone_set = _convert_audio_and_split_sentences(work_dir, "test", "test-wav", "test-txt", phone_set)

    # Write sets to disk as CSV files
    train_df.to_csv(os.path.join(data_dir, "thchs30-train.csv"), index=False,header=False)
    dev_df.to_csv(os.path.join(data_dir, "thchs30-dev.csv"), index=False,header=False)
    test_df.to_csv(os.path.join(data_dir, "thchs30-test.csv"), index=False,header=False)
    json.dump(list(phone_set), open(os.path.join(data_dir,"thchs30_phone_set.json"),'w'), indent=4)

def _convert_audio_and_split_sentences(extracted_dir, data_set, dest_dir, dest_dir2, phone_set):
    source_dir = os.path.join(extracted_dir, data_set)
    target_dir = os.path.join(extracted_dir, dest_dir)
    target_txt_dir = os.path.join(extracted_dir, dest_dir2)

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    if not os.path.exists(target_txt_dir):
        os.makedirs(target_txt_dir)

    files = []
    for root, dirnames, filenames in os.walk(source_dir):
        print(root, dirnames, len(filenames))
        for filename in fnmatch.filter(filenames, '*.trn'):
            tmp_filename = os.path.join(root, filename)
            target_line = 3
            with open(tmp_filename, "r") as fin:
                target_file = os.path.join(root, fin.readline().strip())
            with open(target_file, "r") as fin:
                while target_line > 0:
                    line = fin.readline().strip()
                    target_line -= 1
                    # Parse each segment line
                transcript = line.split(' ')
                phone_set = phone_set | set(transcript)
                wav_file = os.path.join(target_dir,  filename[:-8]+'.wav')
                txt_file = os.path.join(target_txt_dir, filename[:-8]+".txt")
                txt_fid = open(txt_file,'w')
                for phone in transcript:
                    txt_fid.write(phone+'\n')
                txt_fid.close()
                if not os.path.exists(wav_file):
                    os.system('cp '+target_file[:-4]+' '+wav_file)
                    # wav_filesize = os.path.getsize(wav_file)

                files.append((os.path.abspath(wav_file), os.path.abspath(txt_file)))

    return pandas.DataFrame(data=files, columns=["wav_filename", "txt_filename"]), phone_set

if __name__ == "__main__":
    _preprocess_data('/data5/hyzhan/data/thchs30')

# thchs30
# |-- data
# |-- dev
# |-- lm_phone
# |-- lm_word
# |-- README.TXT
# |-- test
# `-- train

