# -*- coding: utf-8 -*-
import os
import argparse as ap
import fnmatch
from utils import update_progress


if __name__ == "__main__":
    # Argument Parser
    parser = ap.ArgumentParser()
    parser.add_argument(
        "--input",
        help="Path to input video files default = /../data/mp4/",
        required=True)
    parser.add_argument(
        "--output",
        help="Path to output wav files default = /../data/origin2/",
        default='output')
    args = vars(parser.parse_args())
    input_dir = os.path.join(os.getcwd(), args["input"])
    print input_dir
    for root, root_dir_names, root_file_names in os.walk(input_dir):
        print root, root_dir_names, len(root_file_names)
        curr_num = 0
        file_num = len(root_file_names) 
        for file_name in fnmatch.filter(root_file_names, '*.txt'):
            file_path = os.path.join(root, file_name) 
            file_str = open(file_path,'r').read().strip()
            # print(file_str)
            fid = open(file_path,'w')
            fid.write(file_str+'.')
            fid.close() 
            curr_num += 1
            update_progress(curr_num / float(file_num))
    print('\n')
