# -*- coding:utf-8 -*-
# !/usr/bin/env python
import os
import argparse as ap
import re


def update_progress(progress):
    print("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(progress * 50),
                                                  progress * 100), end="")


class phoneDict(object):
    def __init__(self, file_path):
        self.phone_dict = self.loadDict(file_path)
        self.mark_dict = {1:'<stop>',2:'<comma>',3:'<question>',4:'<exclam>',5:'<semicolon>',6:'<colon>',7:'<other>'}
        # self.re_list =[r"\w+-\w+", r"\w+'\w+", r"\w+\.\w+",r"\w+\.'\w+",r"\w+\.\w+\."]

    def loadDict(self, file_path):
        fileIn = open(file_path)
        my_dict = {}
        for line in fileIn:
            line = line.replace('  ',' ')
            lineArr = line.rstrip().split(' ')
            my_dict[str(lineArr[0])] = list(lineArr[1:])
        return my_dict

    def txtToDict(self, text):
        pho_result = []
        text = text.strip().lower() 
        res = r"[^a-z]*([a-z]+)[^a-z]*"
        words = re.findall(res, text)
        original = ' '.join(words)
        targets = original.replace(' ', '  ')
        words_list = targets.split(' ')
        # print words_list
        for word in words_list:
            if word == '':
                pho_result.append(['<space>'])
            elif not self.phone_dict.has_key(str(word)):
                return -1
            else:
                pho_result.append(self.phone_dict[str(word)])
        print pho_result
        return pho_result

    def txtToDict2(self, text):
        pho_result = []
        text = text.strip().upper()
        # print("text: %s" % (text))
        if '"' in text:
            text =text.replace('"','')
        if '-' in text:
            text =text.replace('-','')
        if '&' in text:
            return -1
        if '  ' in text:
            text =text.replace('  ',' ')
        res = r"[a-z]+"
        res2 = r"(\w+-\w+)|(\w+'\w+)|(\w+\.\w+\.)|(\w+\.'\w+)|(\w+)"
        words_list = text.split(' ')
        space_num = len(words_list) - 1
        # print words_list
        for words in words_list:
            # for curr_re in self.re_list:
            #     words_mix = re.findall(curr_re, words)
            #     if len(words_mix) > 0:
            #         print("found speacial: %s" % (words_mix))
            #         break
            words_found = re.findall(res2, words)
            if len(words_found) == 0:
                if words == '.':
                    pho_result.append([self.mark_dict[1]])
                elif words == ',':
                    pho_result.append([self.mark_dict[2]])
                elif words == '?':
                    pho_result.append([self.mark_dict[3]])
                elif words == '!':
                    pho_result.append([self.mark_dict[4]])
                elif words == ';':
                    pho_result.append([self.mark_dict[5]])
                elif words == ':':
                    pho_result.append([self.mark_dict[6]])
                else:
                    pho_result.append([self.mark_dict[7]])
                continue
            # print(words_found)
            words_mix = [filter(None, word) for word in words_found]
            if len(words_mix) == 0:
                pass
            else:
                words_mix = words_mix[0]
            # print words, words_mix
            if len(words_mix) == 0:
                words_mix = re.findall(res, words)[0]
            else:
                words_mix = words_mix[0]
            # print words, words_mix
            prefix = 0
            suffix = 0
            if len(words_mix) != len(words):
                if words.startswith(words_mix):
                    if words.endswith('.'):
                        suffix = 1
                    elif words.endswith(','):
                        suffix = 2
                    elif words.endswith('?'):
                        suffix = 3
                    elif words.endswith('!'):
                        suffix = 4
                    elif words.endswith(';'):
                        suffix = 5
                    elif words.endswith(':'):
                        suffix = 6
                    else:
                        suffix = 7
                if words.endswith(words_mix):
                    if words.startswith('.'):
                        prefix = 1
                    elif words.startswith(','):
                        prefix = 2
                    elif words.startswith('?'):
                        prefix = 3
                    elif words.startswith('!'):
                        prefix = 4
                    elif words.startswith(';'):
                        prefix = 5
                    elif words.startswith(':'):
                        prefix = 6
                    else:
                        prefix = 7
            # print prefix,suffix
            if prefix > 0:
                pho_result.append([self.mark_dict[prefix]])
            if not self.phone_dict.has_key(str(words_mix)):
                # print(text)
                # print("failed word: %s" % (words_mix))
                return -1
            else:
                pho_result.append(self.phone_dict[str(words_mix)])
            if suffix > 0:
                pho_result.append([self.mark_dict[suffix]])
            if space_num > 0:
                if suffix == 0:
                    pho_result.append(['<space>'])
                space_num -= 1
        # print pho_result
        return pho_result


if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument("--output",help="Path to input files", default="output") 
    parser.add_argument("--wav_dir", default='txt', type=str, help="Directory to store the dataset.")
    parser.add_argument("--txt_dir", default='wav', type=str, help="Directory to store the dataset.")

    args = vars(parser.parse_args())
    input_txt_dir = args["txt_dir"]  # 输入文件夹中的txt文件夹
    input_wav_dir = args["wav_dir"]  # 输入文件夹中的wav文件夹
    output_phone_dir = os.path.join(args["output"], 'phone-txt')  # 输出音素文件为输出文件夹下phone文件夹
    if not os.path.isdir(output_phone_dir):
        os.makedirs(output_phone_dir)
    output_wav_dir = os.path.join(args["output"], 'phone-wav')
    if not os.path.isdir(output_wav_dir):
        os.makedirs(output_wav_dir)
    dict_class = phoneDict('cmudict-0.7b')  # 读音素字典
    print("test word: %s : %s " % ('hello',dict_class.txtToDict2("do you see a man skilled in his work? he will serve kings. he won't serve obscure men.")))  # 字典测试
    input_files = os.listdir(input_txt_dir)
    data_num = 0
    total_num = len(input_files)
    for index,file_name in enumerate(input_files):
        # break
        # print("Processing: %s" % (file_name))
        lines = open(os.path.join(input_txt_dir, file_name)).readlines()
        fid = open(os.path.join(output_phone_dir, file_name),'w')
        for line in lines:
            line = line.strip()
            word_content = dict_class.txtToDict2(line)
            if word_content == -1:  # 若存在不能识别的单词标记为-1，删除正在写的音素文件，不拷贝wav文件
                fid.close()
                os.system("rm "+os.path.join(output_phone_dir, file_name))
                # print("failed: %s " % (file_name))
                break
            # print(line)
            content = ''
            # print word_content
            for word in word_content:
                for phone in word:
                    if len(phone) > 0:
                        content += phone+' '
                        fid.write(phone+'\n')
            # print(content)
        if word_content != -1:
            fid.close()
            os.system("cp "+os.path.join(input_wav_dir, file_name[:-4]+'.wav')+' '+os.path.join(output_wav_dir, file_name[:-4]+'.wav'))
            data_num += 1
        update_progress(index/float(total_num))
        
    print("total copy data_num: %d" % (data_num))
