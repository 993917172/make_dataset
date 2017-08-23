# -*- coding:utf-8 -*-
# !/usr/bin/env python
import argparse as ap
import json

if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument("--dict_file", default='input', help="Path to input mark files")
    parser.add_argument("--label_file", default="output", help="Path to output file") 

    args = vars(parser.parse_args())
    dict_file = args["dict_file"]
    label_file = args["label_file"]
    
    fid = file(dict_file)
    dictionary = json.load(fid)
    labels_list = ['_']
    mark_list = []
    for labels in dictionary.values():
        # print(labels)
        for label in labels:
            if '<' in label:
                mark_list.append(label)
            else:
                labels_list.append(label)
    # print(labels_list)
    labels = sorted(set(' '.join(labels_list).split(' ')))
    print(mark_list)
    for mark in set(mark_list):
        labels.append(mark)
    labels.append('<space>')
    json.dump(labels, open(label_file, 'w'), indent=4)
    print(labels)
    print(len(labels))