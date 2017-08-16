# -*- coding: utf-8 -*-
import os
import argparse as ap
import scipy.io.wavfile as wav


if __name__ == "__main__":
    # Argument Parser
    parser = ap.ArgumentParser()
    parser.add_argument(
        "--input",
        help="Path to input wav dir",
        required=True)
    parser.add_argument(
        "--input_file",
        help="Path to input wav dir",
        required=True)
    args = vars(parser.parse_args())
    input_dir = os.path.join(os.getcwd(), args["input"])
    input_files = open(args["input_file"], mode='r').readlines()
    print input_dir
    print "开始计算wav时间"
    file_num = 0
    output_time = 0
    for file_name in input_files:
        file_num  += 1
        (rate, sig) = wav.read(os.path.join(input_dir, file_name.strip()+'.wav'))
        target_file_length = int(len(sig) * (1.0/rate))
        output_time += target_file_length
    print " %s 下wav文件时长为：%d秒，%d分, wav文件数量: %d " % (args["input"], output_time, output_time/60, file_num)

