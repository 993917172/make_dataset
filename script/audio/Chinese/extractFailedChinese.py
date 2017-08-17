# -*- coding:utf-8 -*-
# !/usr/bin/env python
import os
import argparse as ap
import re
import json
from multiprocessing import Pool as mp


def update_progress(progress):
    print("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(progress * 50),
                                                  progress * 100), end="")
    
class phoneDict(object):
    def __init__(self, file_path):
        self.phone_dict = self.loadDict(file_path)

    def loadDict(self, file_path):
        fileIn = file(file_path)
        my_dict = json.load(fileIn)
        return my_dict

def _convert_transcription(phone_dict, line, output_txt_file):
    pass_flag = True
    failed_words = ''
    fid = open(output_txt_file, 'w')
    for word in line:
        if word in phone_dict:
            continue 
        else:
            pass_flag = False
            failed_words += word
    if not pass_flag:
        fid.write(failed_words.encode('utf-8')+'\n')
        fid.close()
    else:
        fid.close()
        if os.path.exists(output_txt_file):
            os.system('rm '+output_txt_file)


if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument("--output",help="Path to input files", default="output") 
    parser.add_argument("--txt_dir", default='wav', type=str, help="Directory to store the dataset.")
    parser.add_argument("--dict_file", default='Chinese_phone_dict1.json', type=str, help="Directory to store the dataset.")

    args = vars(parser.parse_args())
    input_txt_dir = args["txt_dir"]  # input txt dir
    dict_file = args["dict_file"]
    output_txt_dir =  args["output"]   # output failed transform phone txt dir
    if not os.path.isdir(output_txt_dir):
        os.makedirs(output_txt_dir)

    dict_class = phoneDict(dict_file)  # load phone dict
    input_files = os.listdir(input_txt_dir)
    data_num = 0
    total_num = len(input_files)
    processers = mp(32)
    for index,file_name in enumerate(input_files):
        # print("Processing: %s" % (file_name))
        lines = open(os.path.join(input_txt_dir, file_name)).readlines()
        # wavfile_path = os.path.join(input_wav_dir, file_name[:-4]+'.wav')
        # output_wav_file = os.path.join(output_wav_dir, file_name[:-4]+'.wav') 
        output_txt_file = os.path.join(output_txt_dir, file_name) 
        for line in lines:
            line = line.strip()
            # print(line)
            try:
                line = line.decode('utf-8', 'ignore').strip()
            except:
                print("failed decode %s " % (file_name))
                continue
            processers.apply_async(_convert_transcription,args=(dict_class.phone_dict, line, output_txt_file))
            # _convert_transcription(dict_class.phone_dict, line, txtfile_path, output_txt_file, failed_txt_file)
    processers.close()
    processers.join()
    target_file = os.path.join(output_txt_dir, 'expand_words.txt')   
    if os.path.exists(target_file):
       os.system('rm '+target_file)
    output_files = os.listdir(output_txt_dir)
    fid = open(target_file, 'a')
    content = set()
    total_num = len(output_files)
    for index,file_name in enumerate(output_files):
        tmp_file = os.path.join(output_txt_dir, file_name)
        # print("Processing: %s" % (file_name))
        lines = open(tmp_file).readlines()
        for line in lines:
            line = line.strip()
            # print(line)
            try:
                line = line.decode('utf-8', 'ignore').strip()
            except:
                print("failed decode %s " % (file_name))
                continue
            # print(line)
            for word in line:
                if word not in content:
                    fid.write(word.encode('utf-8')+'\n')
                # fid.write(line+'\n')
                # if os.path.exists(tmp_file):
                #     os.system('rm '+tmp_file)
                content.add(word)
        update_progress(index/float(total_num))
        # if os.path.exists(tmp_file):
        #     os.system('rm '+tmp_file)
    # update_progress(index/float(total_num))
    for word in sorted(content):
         fid.write(word.encode('utf-8')+'\n')
    print(sorted(content))
    print(len(content))
    fid.close()
    print("generated expand_words.txt")
