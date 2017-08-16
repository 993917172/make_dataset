#!/usr/bin/env python
from __future__ import absolute_import, division, print_function

# Make sure we can import stuff from util/
# This script needs to be run from the root of the DeepSpeech repository
import os
import fnmatch
import pandas
import subprocess
import unicodedata
import json,re
from utils import update_progress
from multiprocessing import Pool as mp
from TextToPhoneme import phoneDict


def _preprocess_data(data_dir):
    print("Splitting transcriptions and convert wav...")
    train = _convert_audio_and_split_sentences(data_dir, "train", "train-phone-wav", "train-phone-txt")
    dev = _convert_audio_and_split_sentences(data_dir, "dev", "dev-phone-wav", "dev-phone-txt")
    test = _convert_audio_and_split_sentences(data_dir, "test", "test-phone-wav", "test-phone-txt")

    # for i in range(text_len):
    #     tmp_line = texts_df.iloc[i, :]
    #     processers.apply_async(_convert_audio_and_split_sentences, args=(data_dir, target_dir, target_txt_dir, checkClass, tmp_line[0], tmp_line[1]))
    # processers.close()
    # processers.join()
    # Write sets to disk as CSV files
    train.to_csv(os.path.join(data_dir, "TED-train-phone.csv"), index=False, header=False)
    dev.to_csv(os.path.join(data_dir, "TED-dev-phone.csv"), index=False, header=False)
    test.to_csv(os.path.join(data_dir, "TED-test-phone.csv"), index=False, header=False)


def _convert_audio_and_split_sentences(extracted_dir, data_set, dest_dir, dest_dir2):
    source_dir = os.path.join(extracted_dir, data_set)
    target_dir = os.path.join(extracted_dir, dest_dir)
    target_txt_dir = os.path.join(extracted_dir, dest_dir2) 
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    if not os.path.exists(target_txt_dir):
        os.makedirs(target_txt_dir)
    processers = mp(8)
    checkClass = phoneDict('cmudict-0.7b')
    res = r"(.*)\s+(\d+)\s+(.*)\s+(.*)\s+(.*)\s+(<.*>)\s+(.*)"
    for root, dirnames, filenames in os.walk(source_dir):
        print(root, dirnames, len(filenames))
        for filename in fnmatch.filter(filenames, '*.stm'):
            trans_filename = os.path.join(root, filename)
            sph_filename = trans_filename.replace('stm','sph')
            # print(sph_filename,trans_filename)
            lines = open(trans_filename, 'r').readlines()
            for index, line in enumerate(lines):
                # print(line)
                processers.apply_async(_check_and_save_wav, args=(sph_filename, target_dir, target_txt_dir, checkClass, line, res, index))
                # _check_and_save_wav(sph_filename, target_dir, target_txt_dir, checkClass, line, res, index)
    processers.close()
    processers.join()
    files = []
    wav_filenames = [i[:-4] for i in os.listdir(target_dir)]
    txt_filenames = [i[:-4] for i in os.listdir(target_txt_dir)]
    file_names = list(set(wav_filenames) & set(txt_filenames))
    for file_name in file_names:
        files.append((os.path.abspath(os.path.join(target_dir, file_name+".wav")), os.path.abspath(os.path.join(target_txt_dir, file_name+".txt"))))
    return pandas.DataFrame(data=files, columns=["wav_filename", "txt_filename"])

def _check_and_save_wav(sph_filename, target_dir, target_txt_dir, checkClass, line, res, index):
    extract_list = re.findall(res, line)[0]
    # print(extract_list)
    text = extract_list[-1].strip()
    if "ignore_time" in text:
        return
    word_content = checkClass.txtToDict2(text)
    if word_content != -1:
        base_name = extract_list[0]
        wav_filename = os.path.join(target_dir, base_name+'_'+str(index).zfill(3)+'.wav')
        txt_filename = os.path.join(target_txt_dir, base_name+'_'+str(index).zfill(3)+'.txt')
        fid = open(txt_filename, 'w')
        content = ''
        for word in word_content:
            for phone in word:
                if len(phone) > 0:
                    content += phone+' '
                    fid.write(phone+'\n')
        fid.close()
        # print(content)
        if not os.path.exists(wav_filename):
            start_time = float(extract_list[3])-0.2
            duration = float(extract_list[4]) - start_time + 0.2
            os.system("sox "+sph_filename+" -r 16000 "+wav_filename+' trim '+str(start_time)+' '+str(duration))


if __name__ == "__main__":
    _preprocess_data('/data5/hyzhan/data/TEDLIUM_release2')
