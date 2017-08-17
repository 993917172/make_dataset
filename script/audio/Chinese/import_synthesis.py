#!/usr/bin/env python
from __future__ import absolute_import, division, print_function

# Make sure we can import stuff from util/
# This script needs to be run from the root of the DeepSpeech repository
import os
import fnmatch
import pandas
from multiprocessing import Pool as mp


def _preprocess_data(data_dir, output_dir):
    print("Splitting transcriptions and convert wav...")
    processers = mp(32)
    # texts_df = pandas.read_table(os.path.join(data_dir, 'text.csv'), sep=',', names=['filename', 'text', 'score'])
    # text_len = len(texts_df)
    # checkClass = phoneDict('cmudict-0.7b')
    target_wav_dir = os.path.join(output_dir, "synthesis-wav")
    target_txt_dir = os.path.join(output_dir, "synthesis-txt")
    if not os.path.exists(target_wav_dir):
        os.makedirs(target_wav_dir)
    if not os.path.exists(target_txt_dir):
        os.makedirs(target_txt_dir)

    total_num = 0
    for root, root_dir_names, root_file_names in os.walk(data_dir):
        print(root, root_dir_names, len(root_file_names))
        for file_name in fnmatch.filter(root_file_names, '*.txt'):
            total_num += 1
            file_path = os.path.join(root, file_name)
            output_txt_file = os.path.join(target_txt_dir, str(total_num).zfill(6)+'.txt')
            mp3file_path = os.path.abspath(os.path.join(root, file_name[:-4]+'.mp3'))
            output_wav_file = os.path.join(target_wav_dir, str(total_num).zfill(6)+'.wav')
            # print(file_path, mp3file_path, output_wav_file, output_txt_file)
            processers.apply_async(_convert_audio, args=(file_path, mp3file_path, output_wav_file, output_txt_file))
    processers.close()
    processers.join()
    files = []
    wav_filenames = [i[:-4] for i in os.listdir(target_wav_dir)]
    txt_filenames = [i[:-4] for i in os.listdir(target_txt_dir)]
    file_names = list(set(wav_filenames) & set(txt_filenames))
    for file_name in file_names:
        files.append((os.path.abspath(os.path.join(target_wav_dir, file_name+".wav")), os.path.abspath(os.path.join(target_txt_dir, file_name+".txt"))))
    # Write sets to disk as CSV files
    data_df = pandas.DataFrame(data=files, columns=["wav_filename", "txt_filename"])
    data_df.to_csv(os.path.join(output_dir, "synthesis.csv"), index=False, header=False)


def _convert_audio(file_path, mp3file_path, output_wav_file, output_txt_file):
    if not os.path.exists(output_txt_file):
        os.system('cp '+file_path+' '+output_txt_file)
    if not os.path.exists(output_wav_file):
        os.system('sox '+mp3file_path+' -b 16 -r 16000 '+output_wav_file)
    


if __name__ == "__main__":
    _preprocess_data('/data5/hyzhan/data/data1', '/data5/hyzhan/data/synthesis')
