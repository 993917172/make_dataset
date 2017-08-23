# -*- coding:utf-8 -*-
# !/usr/bin/env python
import os
import argparse as ap
import re
import json
from utils import update_progress
from multiprocessing import Pool as mp


class phoneDict(object):
    def __init__(self, file_path):
        self.phone_dict = self.loadDict(file_path)

    def loadDict(self, file_path):
        fileIn = file(file_path)
        my_dict = json.load(fileIn)
        return my_dict

    def txtToDict2(self, text):
        pho_result = []
        try:
            text = text.decode('utf8','ignore')
        except:
            try:
                text = text.decode('gbk','ignore')
            except:
                return -1
        # print("text: %s" % (text))
        # print words_list
        for word in text:
            # for curr_re in self.re_list:
            #     words_mix = re.findall(curr_re, words)
            #     if len(words_mix) > 0:
            #         print("found speacial: %s" % (words_mix))
            #         break
            if word in self.phone_dict:
                pho_result.append([self.phone_dict[word]])
            else:
                return -1
        return pho_result

def _convert_transcription(phone_dict, line, txtfile_path, failed_txt_file):
    pass_flag = True
    failed_words = ''
    failed_list = []
    content = []
    for word in line:
        if word in phone_dict:
            hasPhone = phone_dict[word]
            if len(hasPhone) > 1:
                pass_flag = False
                failed_words += word
                failed_list.append(' '.join(hasPhone))
                content.append('###'+','.join(hasPhone))
            else:
                content.append(hasPhone[0])
        else:
            pass_flag = False
            failed_words += word
            failed_list.append('#')
            content.append('@@@')
    if not pass_flag:
        if not os.path.exists(failed_txt_file):
            fid2 = open(failed_txt_file, 'w')
            print(line,content)
            for word,phone in zip(line, content):
                fid2.write(word.encode('utf-8')+' '+phone.encode('utf-8')+'\n')
            fid2.close()
    # if not os.path.exists(output_wav_file):
    #     os.system('cp '+wavfile_path+' '+output_txt_file)


if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument("--output",help="Path to input files", default="output") 
    parser.add_argument("--txt_dir", default='wav', type=str, help="Directory to store the dataset.")
    parser.add_argument("--dict_file", default='Chinese_phone_dict1.json', type=str, help="Directory to store the dataset.")

    args = vars(parser.parse_args())
    input_txt_dir = args["txt_dir"]  # 输入文件夹中的txt文件夹
    dict_file = args["dict_file"]
    failed_txt_dir = os.path.join(args["output"], 'fix-failed-txt')  # 输出音素文件为输出文件夹下phone文件夹
    if not os.path.isdir(failed_txt_dir):
        os.makedirs(failed_txt_dir)
    # failed_wav_dir = os.path.join(args["output"], 'failed-wav')
    # if not os.path.isdir(failed_wav_dir):
    #     os.makedirs(failed_wav_dir)

    dict_class = phoneDict(dict_file)  # 读音素字典
    print("test word: %s : %s " % ('hello',dict_class.txtToDict2("今天。")))  # 字典测试
    input_files = os.listdir(input_txt_dir)
    data_num = 0
    total_num = len(input_files)
    processers = mp(32)
    for index,file_name in enumerate(input_files):
        # break
        # print("Processing: %s" % (file_name))
        lines = open(os.path.join(input_txt_dir, file_name)).readlines()
        # wavfile_path = os.path.join(input_wav_dir, file_name[:-4]+'.wav')
        txtfile_path = os.path.join(input_txt_dir, file_name)
        # output_wav_file = os.path.join(output_wav_dir, file_name[:-4]+'.wav') 
        failed_txt_file = os.path.join(failed_txt_dir, file_name)
        line = lines[0].strip()
        try:
            line = line.decode('utf-8', 'ignore').strip()
        except:
            print("failed decode %s " % (file_name))
            continue
        print(line)
        # processers.apply_async(_convert_transcription,args=(dict_class.phone_dict, line, txtfile_path, failed_txt_file))
        _convert_transcription(dict_class.phone_dict, line, txtfile_path, failed_txt_file)
    processers.close()
    processers.join()
    # update_progress(index/float(total_num))  
    # print("total copy data_num: %d" % (data_num))
