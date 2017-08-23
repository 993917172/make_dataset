# -*- coding:utf-8 -*-
# !/usr/bin/env python
import os
import fnmatch
import argparse as ap
import re

if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument("--input_file", default='input', help="Path to input mark files")
    parser.add_argument("--input", default='input', help="Path to input mark files")
    parser.add_argument("--output_file", default="output", help="Path to output file") 

    args = vars(parser.parse_args())
    input_dir = args["input"]
    input_file = args["input_file"]
    output_file = args["output_file"]
    fid = open(output_file, 'w')
    origin_lines = open(input_file).readlines()
    origin_list = []
    for line in origin_lines:
        origin_list.append(line.strip().decode('utf-8'))
    origin_list = set(origin_list)
    res = u'([\u4e00-\u9fa5]+)\s(.+)'
    add_word = 0
    add_list = []
    for root, root_dir_names, root_file_names in os.walk(input_dir):
        for file_name in fnmatch.filter(root_file_names, '*.txt'):
            print("Processing: %s " % (file_name))
            file_path = os.path.join(root, file_name)
            lines = open(file_path, 'r').readlines()
            for line in lines:
                line = line.strip().decode('utf-8')
                word, label_str = re.findall(res, line)[0]
                labels = label_str.split(',')
                for label in labels:
                    add_list.append(label.strip())
    add_list = set(add_list)
    # print(origin_list)
    result_list = origin_list | add_list
    result_list = sorted(list(result_list))
    for label in result_list:
        fid.write(label+'\n')
    print(len(origin_list), len(result_list))