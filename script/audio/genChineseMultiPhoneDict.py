# -*- coding: utf-8 -*-
import os
import fnmatch
import argparse as ap
import json
import re

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
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    print input_dir
    Chinese = u'[\u4e00-\u9fa5]+'
    Chinese_phone_dict1 = {}
    Chinese_phone_dict2 = {}
    Chinese_phone2phone_dict = {}
    fail_word = 0
    total_word = 0
    for root, root_dir_names, root_file_names in os.walk(input_dir):
        print root, root_dir_names, len(root_file_names)
        for filename in fnmatch.filter(root_file_names, '*.trn'):
            # print("Processing: %s " % (filename))
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
                # print(Chinese_words)
                Chinese_words = Chinese_words.decode('utf8', 'ignore')
            except:
                try:
                    Chinese_words = Chinese_words.decode('gb2312', 'ignore').strip()
                    # print('gb2312')
                except:
                    try:
                        Chinese_words = Chinese_words.decode('utf8', 'ignore').strip()
                        # print('utf8')
                    except:
                        # print line
                        print("%s failed." % (filename))
                        # print chardet.detect(line)
                        continue
            # print(len(Chinese_words), len(phone1_list), len(phone2_list))
            total_word += len(phone1_list)
            if 2*len(phone1_list) != len(phone2_list):
                print(filename)
                print(Chinese_words)
                continue
            if len(phone1_list) != len(Chinese_words):
                # print(filename)
                # print(Chinese_words)
                tmp_list = re.findall(Chinese, Chinese_words)
                Chinese_words = ''.join(tmp_list)
                if len(phone1_list) != len(Chinese_words):
                    fail_word += len(phone1_list)
                    continue
            # print(Chinese_words)
            for index, word in enumerate(Chinese_words):
                # print(index, len(Chinese_words))
                if word in Chinese_phone_dict1:
                    Chinese_phone_dict1[word].add(phone1_list[index])
                else:
                    Chinese_phone_dict1[word] = set([phone1_list[index]])
                if word in Chinese_phone_dict2:
                    Chinese_phone_dict2[word].add(' '.join(phone2_list[index*2:index*2+2]))
                else:
                    Chinese_phone_dict2[word] = set([' '.join(phone2_list[index*2:index*2+2])])
                if phone1_list[index] in Chinese_phone2phone_dict:
                    Chinese_phone2phone_dict[phone1_list[index]].add(' '.join(phone2_list[index*2:index*2+2]))
                else:
                    Chinese_phone2phone_dict[phone1_list[index]] = set([' '.join(phone2_list[index*2:index*2+2])])
            # print("Chinese_phone_dict1 size: %d" % (len(Chinese_phone_dict1)))
            # print("Chinese_phone_dict2 size: %d" % (len(Chinese_phone_dict2)))
    for key in Chinese_phone_dict1.keys():
        Chinese_phone_dict1[key] = list(Chinese_phone_dict1[key])
    for key in Chinese_phone_dict2.keys():
        Chinese_phone_dict2[key] = list(Chinese_phone_dict2[key])
    for key in Chinese_phone2phone_dict.keys():
        Chinese_phone2phone_dict[key] = list(Chinese_phone2phone_dict[key])
    Chinese_phone_dict1[u'\u3002'] = ['<stop>']
    Chinese_phone_dict1[u'\uff0c'] = ['<comma>']
    Chinese_phone_dict1[u'\uff01'] = ['<exclam>']
    Chinese_phone_dict1[u'\uff1f'] = ['<question>']
    Chinese_phone_dict1[u'\u2018'] = ['<quotation>']
    Chinese_phone_dict1[u'\u201c'] = ['<quotation>']
    Chinese_phone_dict1[u'\u201d'] = ['<quotation>']
    Chinese_phone_dict1[u'\u2019'] = ['<quotation>']
    Chinese_phone_dict1[u'\''] = ['<quotation>']
    Chinese_phone_dict1[u'\"'] = ['<quotation>']
    Chinese_phone_dict1[u'\uff1a'] = ['<colon>']
    Chinese_phone_dict1[u'\uff1b'] = ['<semicolon>']
    Chinese_phone_dict1[u'\u3001'] = ['<pause>']

    Chinese_phone_dict2[u'\u3002'] = ['<stop>']
    Chinese_phone_dict2[u'\uff0c'] = ['<comma>']
    Chinese_phone_dict2[u'\uff01'] = ['<exclam>']
    Chinese_phone_dict2[u'\uff1f'] = ['<question>']
    Chinese_phone_dict2[u'\u2018'] = ['<quotation>']
    Chinese_phone_dict2[u'\u201c'] = ['<quotation>']
    Chinese_phone_dict2[u'\u201d'] = ['<quotation>']
    Chinese_phone_dict2[u'\u2019'] = ['<quotation>']
    Chinese_phone_dict2[u'\''] = ['<quotation>']
    Chinese_phone_dict2[u'\"'] = ['<quotation>']
    Chinese_phone_dict2[u'\uff1a'] = ['<colon>']
    Chinese_phone_dict2[u'\uff1b'] = ['<semicolon>']
    Chinese_phone_dict2[u'\u3001'] = ['<pause>']
    json.dump(Chinese_phone_dict1, open(args["output"]+'/Chinese_multiphone_dict1.json', 'w'), indent=4)
    json.dump(Chinese_phone_dict2, open(args["output"]+'/Chinese_multiphone_dict2.json', 'w'), indent=4)
    json.dump(Chinese_phone2phone_dict, open(args["output"]+'/Chinese_phone2phone_dict.json', 'w'), indent=4)
    print("fail_word: %d" % (fail_word)) 
    print("total_word: %d" % (total_word)) 
    print("finished")
