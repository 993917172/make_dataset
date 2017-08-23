# -*- coding:utf-8 -*-
# !/usr/bin/env python
import os
import argparse as ap
import re

if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument("--input_file", help="Path to input files", default="3500.txt") 
    parser.add_argument("--expand_file", default='expand_words.txt', type=str, help="expand_words")
    parser.add_argument("--output_file", help="Path to input files", default="usual_Chinese.txt") 

    args = vars(parser.parse_args())
    input_file = args["input_file"]
    expand_file = args["expand_file"]
    output_file = args["output_file"]
    Chinese = u'[\u4e00-\u9fa5]+'
    f1 = open('7000.txt', 'rb').readlines()
    # f1 = open(input_file, 'rb').read().decode('utf-8')
    # lines = re.findall(Chinese, f1)
    f2 = open(expand_file, 'rb').readlines()
    f2 = open(expand_file, 'rb').readlines()
    f4 = open('new.txt', 'rb').read().decode('utf-8')
    lines = re.findall(Chinese, f4)
    set1 = set()
    set2 = set()
    set4 = set()
    for line in f1:
    # for line in lines:
        set1.add(line.strip().decode('utf-8'))
    for line in f2:
        set2.add(line.strip().decode('utf-8'))
    for line in lines:
        set4.add(line.strip())
    set3 = set1 & set2
    print(len(set1), len(set2), len(set3))
    set5 = set3 - set4
    print(len(set3), len(set4), len(set5))
    f3 = open(output_file, 'w')
    lines = '\n'.join(sorted(list(set5))).encode('utf-8')
    f3.write(lines)
    f3.close()
    # print(set1, set2)
