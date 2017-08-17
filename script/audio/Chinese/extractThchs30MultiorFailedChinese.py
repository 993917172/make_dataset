# -*- coding:utf-8 -*-
# !/usr/bin/env python
import os
import argparse as ap
import re
import json
import fnmatch


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
    parser.add_argument("--output", help="Path to output files", default="output") 
    parser.add_argument("--input", default='txt', type=str, help="Path to input files.")
    parser.add_argument("--dict_file", default='Chinese_phone_dict1.json', type=str, help="Directory to store the dataset.")

    args = vars(parser.parse_args())
    input_dir = args["input"]  # 输入文件夹中的wav文件夹
    dict_file = args["dict_file"]
    output_txt_dir = os.path.join(args["output"], 'failed-txt')  # 输出音素文件为输出文件夹下phone文件夹
    if not os.path.isdir(output_txt_dir):
        os.makedirs(output_txt_dir)
    output_wav_dir = os.path.join(args["output"], 'failed-wav')
    if not os.path.isdir(output_wav_dir):
        os.makedirs(output_wav_dir)
    dict_class = phoneDict(dict_file)  # 读音素字典
    print("test word: %s : %s " % ('hello', dict_class.txtToDict2("今天天气真好，希望程序不会出现错误。")))  # 字典测试
    data_num = 0
    Chinese = u'[\u4e00-\u9fa5]+'
    for root, root_dir_names, root_file_names in os.walk(input_dir):
        print root, root_dir_names, len(root_file_names)
        for filename in fnmatch.filter(root_file_names, '*.trn'):
            # print("Processing: %s" % (file_name))
            file_path = os.path.join(root, filename)
            try:
                fin = open(file_path, 'r')
                Chinese_words = fin.readline().strip()
                phone1 = fin.readline().strip()
                phone2 = fin.readline().strip()
                fin.close()
            except:
                print("Failed open %s" % (filename))            
                continue
            Chinese_words = Chinese_words.replace(' ', '')
            phone1_list = phone1.split(' ')
            phone2_list = phone2.split(' ')
            try:
                Chinese_words = Chinese_words.decode('utf8', 'ignore').strip()
            except:
                try:
                    Chinese_words = Chinese_words.decode('gb2312', 'ignore').strip()
                except:
                    continue
            if 2*len(phone1_list) != len(phone2_list):
                continue
            if len(phone1_list) != len(Chinese_words):
                tmp_list = re.findall(Chinese, Chinese_words)
                Chinese_words = ''.join(tmp_list)
                if len(phone1_list) != len(Chinese_words):
                    continue
            pass_flag = True
            failed_words = ''
            failed_list = []
            for word in Chinese_words:
                if word in dict_class.phone_dict:
                    hasPhone = dict_class.phone_dict[word]
                    if len(hasPhone) > 1:
                        pass_flag = False
                        failed_words += word
                        failed_list.append(' '.join(hasPhone))
                else:
                    pass_flag = False
                    failed_words += word
                    failed_list.append('#')
            if pass_flag:
                # fid.close()
                # os.system("rm "+os.path.join(output_phone_dir, file_name))
                # print("failed: %s " % (file_name))
                continue
            fid = open(os.path.join(output_txt_dir, filename[:-8]+'.txt'), 'w')
            # print(Chinese_words)
            fid.write(Chinese_words.encode('utf-8')+'\n')
            fid.write(failed_words.encode('utf-8')+'\n')
            fid.write(','.join(failed_list).encode('utf-8')+'\n')
            fid.close()
            wav_file = os.path.join(output_wav_dir, filename[:-4])
            if not os.path.exists(wav_file):
                os.system("cp "+file_path[:-4]+' '+wav_file)
            data_num += 1
        
    print("total copy data_num: %d" % (data_num))
