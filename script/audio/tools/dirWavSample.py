# -*- coding: utf-8 -*-
import os
import argparse as ap

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
        if len(root_file_names) > 0:
            for file_name in root_file_names:
                if file_name.endswith('wav'):
                    file_path = os.path.join(root, file_name)
                    os.system('sox '+file_path+' -b 16 -r 16000 '+'tmp.wav')
                    os.system('cp tmp.wav '+file_path)
