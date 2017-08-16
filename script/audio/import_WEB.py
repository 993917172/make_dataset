#!/usr/bin/env python
from __future__ import absolute_import, division, print_function

# Make sure we can import stuff from util/
# This script needs to be run from the root of the DeepSpeech repository
import os
import fnmatch
import pandas
import subprocess
import unicodedata
import json
from utils import update_progress
from multiprocessing import Pool as mp
from TextToPhoneme import phoneDict


def _preprocess_data(data_dir, output_dir):
    print("Splitting transcriptions and convert wav...")
    processers = mp(4)
    texts_df = pandas.read_table(os.path.join(data_dir, 'text.csv'), sep=',', names=['filename', 'text', 'score'])
    text_len = len(texts_df)
    checkClass = phoneDict('cmudict-0.7b')
    target_dir = os.path.join(output_dir, "wav")
    target_txt_dir = os.path.join(output_dir, "txt")
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    if not os.path.exists(target_txt_dir):
        os.makedirs(target_txt_dir)
    for i in range(text_len):
        tmp_line = texts_df.iloc[i, :]
        processers.apply_async(_convert_audio_and_split_sentences, args=(data_dir, target_dir, target_txt_dir, checkClass, tmp_line[0], tmp_line[1]))
    processers.close()
    processers.join()
    files = []
    wav_filenames = [i[:-4] for i in os.listdir(target_dir)]
    txt_filenames = [i[:-4] for i in os.listdir(target_txt_dir)]
    file_names = list(set(wav_filenames) & set(txt_filenames))
    for file_name in file_names:
        files.append((os.path.abspath(os.path.join(target_dir, file_name+".wav")), os.path.abspath(os.path.join(target_txt_dir, file_name+".txt"))))
    # Write sets to disk as CSV files
    data_df = pandas.DataFrame(data=files, columns=["wav_filename", "txt_filename"])
    data_df.to_csv(os.path.join(output_dir, "WEB.csv"), index=False, header=False)


def _convert_audio_and_split_sentences(data_dir, target_dir, target_txt_dir, checkClass, filename, text):
    
    word_content = checkClass.txtToDict2(text)
    if word_content != -1:
        wav_filename = os.path.join(data_dir, filename+'.wav')
        base_name = os.path.basename(wav_filename)[:-4]
        txt_filename = os.path.join(target_txt_dir, base_name+'.txt')
        fid = open(txt_filename, 'w')
        content = ''
        for word in word_content:
            for phone in word:
                if len(phone) > 0:
                    content += phone+' '
                    fid.write(phone+'\n')
        fid.close()
        # print(content)
        os.system("sox "+wav_filename+" -r 16000 "+os.path.join(target_dir, base_name+'.wav'))


if __name__ == "__main__":
    _preprocess_data('/data1/data_all/WEB', '/data1/data_all/WEB-phone')
