# -*- coding: utf-8 -*-
import os
import argparse as ap
import scipy.io.wavfile as wav
import traceback

if __name__ == "__main__":
    # Argument Parser
    parser = ap.ArgumentParser()
    parser.add_argument(
        "--input",
        help="Path to input wav dir",
        required=True)
    args = vars(parser.parse_args())
    input_dir = os.path.join(os.getcwd(), args["input"])
    print input_dir
    print "开始计算wav时间"
    file_num = 0
    rate_set = set()
    output_time = 0
    for root, root_dir_names, root_file_names in os.walk(input_dir):
        print root, root_dir_names, len(root_file_names)
        if len(root_file_names) > 0:
            for file_name in root_file_names:
                if file_name.endswith('wav') or file_name.endswith('WAV'):
                    file_num  += 1
                    try:
                        (rate, sig) = wav.read(os.path.join(root, file_name))
                    except:
                        print(traceback.format_exc())
                        print("pass 1 file")
                        continue
                    rate_set.add(rate)
                    target_file_length = float(len(sig) * (1.0/rate))
                    output_time += target_file_length
    print(rate_set)
    print " %s 下wav文件时长为：%.2f秒，%.2f分, wav文件数量: %d " % (input_dir, output_time, output_time/60, file_num)

