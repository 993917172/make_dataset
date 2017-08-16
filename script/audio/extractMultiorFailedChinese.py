# -*- coding:utf-8 -*-
# !/usr/bin/env python
import os
import argparse as ap
import re
import json
from utils import update_progress


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
            text = text.decode('utf8', 'ignore')
        except:
            try:
                text = text.decode('gbk', 'ignore')
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
                hasPhone = self.phone_dict[word]
                if len(hasPhone) > 1:
                    return -1
                else:
                    pho_result.append([self.phone_dict[word][0]])
            else:
                return -1
        return pho_result


if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument("--output", help="Path to input files", default="output") 
    parser.add_argument("--wav_dir", default='txt', type=str, help="Directory to store the dataset.")
    parser.add_argument("--txt_dir", default='wav', type=str, help="Directory to store the dataset.")
    parser.add_argument("--dict_file", default='Chinese_phone_dict1.json', type=str, help="Directory to store the dataset.")

    args = vars(parser.parse_args())
    input_txt_dir = args["txt_dir"]  # 输入文件夹中的txt文件夹
    input_wav_dir = args["wav_dir"]  # 输入文件夹中的wav文件夹
    dict_file = args["dict_file"]
    output_phone_dir = os.path.join(args["output"], 'phone-txt')  # 输出音素文件为输出文件夹下phone文件夹
    if not os.path.isdir(output_phone_dir):
        os.makedirs(output_phone_dir)
    output_wav_dir = os.path.join(args["output"], 'phone-wav')
    if not os.path.isdir(output_wav_dir):
        os.makedirs(output_wav_dir)
    dict_class = phoneDict(dict_file)  # 读音素字典
    print("test word: %s : %s " % ('hello', dict_class.txtToDict2("今天天气真好，希望程序不会出现错误。")))  # 字典测试
    input_files = os.listdir(input_txt_dir)
    data_num = 0
    total_num = len(input_files)
    for index, file_name in enumerate(input_files):
        # break
        # print("Processing: %s" % (file_name))
        lines = open(os.path.join(input_txt_dir, file_name)).readlines()
        fid = open(os.path.join(output_phone_dir, file_name), 'w')
        for line in lines:
            line = line.strip()
            word_content = dict_class.txtToDict2(line)
            if word_content != -1:  # 若存在不能识别的单词标记为-1，删除正在写的音素文件，不拷贝wav文件
                # fid.close()
                # os.system("rm "+os.path.join(output_phone_dir, file_name))
                # print("failed: %s " % (file_name))
                continue
            print(line)
            fid.write(line+'\n')
            fid.close()
            os.system("cp "+os.path.join(input_wav_dir, file_name[:-4]+'.wav')+' '+os.path.join(output_wav_dir, file_name[:-4]+'.wav'))
            data_num += 1
        update_progress(index/float(total_num))
        
    print("total copy data_num: %d" % (data_num))
