# -*- coding:utf-8 -*-
# !/usr/bin/env python
import os
import argparse as ap
import fnmatch

if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument("--input", default='input', help="Path to input mark files")
    parser.add_argument("--output", default="output", help="Path to output file") 

    args = vars(parser.parse_args())
    input_dir = args["input"]
    output_dir = args["output"]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for root, root_dir_names, root_file_names in os.walk(input_dir):
        for file_name in fnmatch.filter(root_file_names, '*.txt'):
            print("Processing: %s " % (file_name))
            file_path = os.path.join(root, file_name)
            output_file_path = os.path.join(output_dir, file_name)
            lines = open(file_path, 'r').readlines()
            fid = open(output_file_path, 'w')
            for line in lines:
                line = line.strip().decode('utf-8')
                labels = line.split(' ')
                if len(labels) == 2:
                    fid.write(labels[1]+'\n')
                    fid.write('<space>\n')
                else:
                    fid.write(' '.join(labels[1:])+'\n')
                    fid.write('<space>\n')
            fid.close()
