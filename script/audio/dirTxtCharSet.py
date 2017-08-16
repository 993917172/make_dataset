# -*- coding: utf-8 -*-
import os
import argparse as ap
import fnmatch


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
    char_set = set()
    for root, root_dir_names, root_file_names in os.walk(input_dir):
        print root, root_dir_names, len(root_file_names)
        for file_name in fnmatch.filter(root_file_names, '*.txt'):
            file_str = open(os.path.join(root, file_name),'r').read()
            str_set = set(list(file_str))
            char_set = char_set | str_set
    print("char_set: ",char_set)
