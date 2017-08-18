# -*- coding: utf-8 -*-
import os
import argparse as ap
import scipy.io.wavfile as wav


if __name__ == "__main__":
    # Argument Parser
    parser = ap.ArgumentParser()
    parser.add_argument(
        "--input",
        help="Path to input mp4 dir",
        required=True)
    args = vars(parser.parse_args())
    input_dir = os.path.join(os.getcwd(), args["input"])
    print input_dir
    print "开始计算mp4时间"
    file_num = 0
    output_time = 0
    for root, root_dir_names, root_file_names in os.walk(input_dir):
        print root, root_dir_names, len(root_file_names)
        if len(root_file_names) > 0:
            for file_name in root_file_names:
                if file_name.endswith('mp4'):
                    file_num  += 1
                    target_file_length_str = os.popen("ffmpeg -i "+os.path.join(root, file_name)+" 2>&1 | grep 'Duration' | cut -d ' ' -f 4 | sed s/,//").readlines()
                    target_file_length_list = target_file_length_str[0].strip().split(':')
                    target_file_length = float(float(target_file_length_list[0])*3600+float(target_file_length_list[1])*60+float(target_file_length_list[2]))

                    output_time += target_file_length
    print " %s 下wav文件时长为：%.2f秒，%.2f分, wav文件数量: %d " % (root, output_time, output_time/60, file_num)

