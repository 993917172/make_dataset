# -*- coding:utf-8 -*-
# !/usr/bin/env python
import os
import argparse as ap
import re
import json
import fnmatch

if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument("--dict_file", default="Chinese_multiphone_dict2.json", help="Path to input dict file") 
    parser.add_argument("--mark_dir", default='input', help="Path to input mark files")
    parser.add_argument("--expand_type", default="pinyin", help="expand label type")
    parser.add_argument("--output_file", default="new_dict.json", help="Path to output file") 

    args = vars(parser.parse_args())
    dict_file = args["dict_file"]
    mark_dir = args["mark_dir"]
    output_file = args["output_file"]
    Chinese = u'[\u4e00-\u9fa5]+'
    f = file(dict_file)
    Chinese_org_dict = json.load(f)
    # print(Chinese_org_dict)
    org_key_set = set(Chinese_org_dict.keys())
    res = u'([\u4e00-\u9fa5]+)\s(.+)'
    add_word = 0
    multi_word = 0
    
    for root, root_dir_names, root_file_names in os.walk(mark_dir):
        for mark_file in fnmatch.filter(root_file_names, '*.txt'):
            print("Processing: %s " % (mark_file))
            mark_file_path = os.path.join(root, mark_file)
            lines = open(mark_file_path, 'r').readlines()
            if args["expand_type"] == 'pinyin':
                for line in lines:
                    line = line.strip().decode('utf-8')
                    # print(line)
                    # print(re.findall(res, line))
                    try:
                        word, label_str = re.findall(res, line)[0]
                    except:
                        print(line)
                        Exception
                    labels = label_str.split(',')
                    
                    for label in labels:
                        # print(label)
                        if word not in Chinese_org_dict:
                            Chinese_org_dict[word] = [label.split(':')[0]]
                            add_word += 1
                        else:
                            # print(Chinese_org_dict[word])
                            if label.split(':')[0] not in Chinese_org_dict[word]:
                                Chinese_org_dict[word].append(label.split(':')[0])
                                multi_word += 1
            else:
                for line in lines:
                    line = line.strip().decode('utf-8')
                    word, label_str = re.findall(res, line)[0]
                    labels = label_str.split(',')
                    for label in labels:
                        if word not in Chinese_org_dict:
                            Chinese_org_dict[word] = [label.split(':')[1]]
                            add_word += 1
                        else:
                            if label.split(':')[1] not in Chinese_org_dict[word]:
                                Chinese_org_dict[word].append(label.split(':')[1])
                                multi_word += 1

    json.dump(Chinese_org_dict, open(args["output_file"], 'w'), indent=4)
    print("add_word: %d, multi_word: %d " % (add_word, multi_word))
    new_key_set = set(Chinese_org_dict.keys())
    add_set = new_key_set - org_key_set
    print("org_key_set: %d, new_key_set: %d, add_set: %d" % (len(org_key_set), len(new_key_set), len(add_set)))
