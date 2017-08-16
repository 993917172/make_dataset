# -*- coding:utf-8 -*-
# !/usr/bin/env python
import os
import argparse as ap
from multiprocessing import Pool as mp


def checkMiss(file_name, input_dir, suffix):
    if os.path.exists(os.path.join(input_dir, file_name+suffix)):
        os.system('rm '+os.path.join(input_dir, file_name+suffix))

if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument("--wav_dir", default='txt', type=str, help="Directory to store the dataset.")
    parser.add_argument("--txt_dir", default='wav', type=str, help="Directory to store the dataset.")

    args = vars(parser.parse_args())
    input_txt_dir = args["txt_dir"]  # 输入文件夹中的txt文件夹
    input_wav_dir = args["wav_dir"]  # 输入文件夹中的wav文件夹
    wav_filenames = [i[:-4] for i in os.listdir(input_wav_dir)]
    txt_filenames = [i[:-4] for i in os.listdir(input_txt_dir)]
    file_names = set(wav_filenames) & set(txt_filenames)
    print("wav_filenames:%d, txt_filenames:%d, file_names:%d" % (len(wav_filenames), len(txt_filenames),len(file_names)))
    processers = mp(32)
    redundant_wav = set(wav_filenames) - file_names
    redundant_txt = set(txt_filenames) - file_names
    for file_name in redundant_wav:
        processers.apply_async(checkMiss, args=(file_name, input_wav_dir, ".wav"))
    for file_name in redundant_txt:
        processers.apply_async(checkMiss, args=(file_name, input_txt_dir, ".txt"))
        # if file_name not in wav_filenames:
        #     os.system('rm '+os.path.join(input_txt_dir, file_name+".txt"))
        # if file_name not in txt_filenames:
        #     os.system('rm '+os.path.join(input_wav_dir, file_name+".wav"))
    processers.close()
    processers.join()
    print("wav_filenames:%d, txt_filenames:%d, file_names:%d" % (len(wav_filenames), len(txt_filenames), len(file_names)))
