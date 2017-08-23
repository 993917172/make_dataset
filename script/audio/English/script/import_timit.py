#!/usr/bin/env python
from __future__ import absolute_import, division, print_function

# Make sure we can import stuff from util/
# This script needs to be run from the root of the DeepSpeech repository
import os
import fnmatch
import pandas
import numpy as np
import re
import scipy.io.wavfile as wav


def _preprocess_data(data_dir):

    print("Converting SPHERE wav to RIFF wav and splitting transcriptions...")
    work_dir = data_dir
    train = _convert_audio_and_split_sentences(work_dir, "train", "train-wav", "train-txt")
    test = _convert_audio_and_split_sentences(work_dir, "test", "test-wav", "test-txt")

    # Write sets to disk as CSV files
    train.to_csv(os.path.join(data_dir, "timit-train.csv"), index=False, header=False)
    test.to_csv(os.path.join(data_dir, "timit-test.csv"), index=False, header=False)


def _convert_audio_and_split_sentences(extracted_dir, data_set, dest_dir, dest_dir2):
    source_dir = os.path.join(extracted_dir, data_set)
    target_dir = os.path.join(extracted_dir, dest_dir)
    target_txt_dir = os.path.join(extracted_dir, dest_dir2)

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    if not os.path.exists(target_txt_dir):
        os.makedirs(target_txt_dir)

    files = []
    res = '[a-zA-Z]+.*'
    wav_num = 1
    for root, dirnames, filenames in os.walk(source_dir):
        print(root, dirnames, len(filenames))
        for filename in fnmatch.filter(filenames, '*.txt'):
            wav_name = filename.split('.')[0]+'.wav'
            wav_filename = os.path.join(root, wav_name) 
            trans_filename = os.path.join(root, filename)
            fin = open(trans_filename, 'r').readlines()
            txt_file = os.path.join(target_txt_dir, str(wav_num).zfill(6)+'.txt')
            txt_fid = open(txt_file, 'w')
            for line in fin:
                    # Parse each segment line
                transcript = re.findall(res, line)
                if len(transcript) > 0:
                    transcript = transcript[0]
                else:
                    transcript = ''
                transcript = transcript.lower().strip()
                if '"' in transcript:
                    transcript = transcript.replace('"', '')
                # print(transcript)
                txt_fid.write(transcript+'\n')
                txt_fid.close()
                # Convert corresponding SPHERE wav to RIFF WAV
                wav_file = os.path.join(target_dir,  str(wav_num).zfill(6)+'.wav')
                # print(transcript,wav_filename)
                # break
                if not os.path.exists(wav_file):
                    fid = open(wav_filename, 'rb')
                    data = np.fromfile(fid, dtype=np.int16)
                    wav.write(wav_file, 16000, data[512:])

                files.append((os.path.abspath(wav_file), os.path.abspath(txt_file)))
            wav_num += 1

    return pandas.DataFrame(data=files, columns=["wav_filename", "txt_filename"])


if __name__ == "__main__":
    _preprocess_data('/data1/data_all/timit')

# timit
# |-- doc
# |-- readme.doc
# |-- test
# |-- TIMIT_phonemes.Table
# |-- train

