# -*- coding: utf-8 -*-
import os
import fnmatch
import argparse as ap
import re
import json


if __name__ == "__main__":
    # Argument Parser
    parser = ap.ArgumentParser()
    parser.add_argument(
        "--input",
        help="Path to input files",
        default='input')
        # required=True)
    parser.add_argument(
        "--output",
        help="Path to output files",
        default='output')
    args = vars(parser.parse_args())
    input_dir = os.path.join(os.getcwd(), args["input"])
    output_dir = os.path.join(os.getcwd(), args["output"])
    output_txt_dir = os.path.join(output_dir, 'txt')
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    if not os.path.isdir(output_txt_dir):
        os.makedirs(output_txt_dir)
    print input_dir
    res = u"[^\u4e00-\u9fa5。，！？‘“”’\'\"：；、\s]+"
    sentence_re = u"[\u4e00-\u9fa5，‘“\'\"：；、\s]+[。！？]+[”’\'\"]?"
    Chinese = u'[\u4e00-\u9fa5]+'
    punctuation = u'\u3002\uff0c\uff01\uff1f\u2018\u201c\u201d\u2019\uff1a\uff1b'
    ChineseCountDict = {}
    sentence_num = 0
    word_num = 0
    file_num = 0
    for root, root_dir_names, root_file_names in os.walk(input_dir):
        print root, root_dir_names, len(root_file_names)
        for filename in fnmatch.filter(root_file_names, '*.txt'):
            # print("Processing: %s " % (filename.decode('gbk')))
            file_path = os.path.join(root, filename)
            try:
                fin = open(file_path, 'r')
                lines = fin.readlines()
                fin.close()
            except:
                print("Failed open %s" % (filename.decode('gbk')))
                continue
            file_num += 1
            fout = open(os.path.join(output_txt_dir, str(file_num).zfill(6)+'.txt'), 'wb')
            write_num = 0
            for line in lines:
                if ' ' in line:
                    line = line.replace(' ', '')
                try:
                    line = line.decode('gbk', 'ignore').strip()
                    # print('gbk')
                except:
                    try:
                        line = line.decode('gb2312', 'ignore').strip()
                        # print('gb2312')
                    except:
                        try:
                            line = line.decode('utf8', 'ignore').strip()
                            # print('utf8')
                        except:
                            # print line
                            print("%s failed." % (filename.decode('gbk')))
                            # print chardet.detect(line)
                            continue
                        
                if len(line) < 6:
                    continue
                # print(line)
                sentences = re.findall(sentence_re, line)
                for sentence in sentences:
                    if len(sentence) < 6 or len(sentence) > 45:
                        continue
                    # print(sentence)
                    # illegal_words = re.findall(res, sentence)
                    # if len(illegal_words) > 0:
                    #     continue
                    phrases = re.findall(Chinese, sentence)
                    # try:
                    #     words = re.findall(Chinese, sentence)[0]
                    # except Exception:
                    #     print(sentence)
                    #     print 'str(Exception):\t', str(Exception)
                        
                    # print(phrases)
                    sentence_num += 1
                    for words in phrases:
                        for word in words:
                            if word in ChineseCountDict:
                                ChineseCountDict[word] += 1
                            else:
                                ChineseCountDict[word] = 1
                    fout.write(sentence.encode('utf-8')+'\n')
                    write_num += 1
            fout.close()
            # print("ChineseCountDict size: %d" % (len(ChineseCountDict)))
            if write_num == 0:
                print("%s failed." % (filename.decode('gbk')))
            
    json.dump(ChineseCountDict, open(args["output"]+'/ChineseCountDict.json', 'w'), indent=4)
    print("ChineseCountDict size: %d" % (len(ChineseCountDict)))
    print("sentence_num: %d" % (sentence_num))
