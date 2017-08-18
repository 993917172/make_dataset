# -*- coding: utf-8 -*-
import os
import argparse as ap
import re


if __name__ == "__main__":
    # Argument Parser
    parser = ap.ArgumentParser()
    parser.add_argument(
        "--input",
        help="Path to input video files default = /../data/mp4/",
        default='input')
    parser.add_argument(
        "--output",
        help="Path to output wav files default = /../data/origin2/",
        default='origin_mp4')
    args = vars(parser.parse_args())
    input_file = os.path.join(os.getcwd(), args["input"], 'Weekly Address.html')
    output_dir = os.path.join(os.getcwd(), args["output"])
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    print input_file
    print "开始处理Html文件"
    html_str = open(input_file, mode='r').read()
    res_url = r"Weekly\sAddress.*aria-describedby.*href=\"(.+)\">\s?(.*Weekly\sAddress.*)\s?</a>"
    link = re.findall(res_url,  html_str)
    total_link = len(link)
    num = 1
    for url,name in link:
        legal_name = name
        if ' ' in legal_name:
            legal_name = legal_name.replace(" ","_")
        if '/' in legal_name:
            legal_name = legal_name.replace("/","_")
        output_sub_dir = os.path.join(output_dir, legal_name)
        if not os.path.isdir(output_sub_dir):
            os.mkdir(output_sub_dir)
        print("%d/%d Downloading %s" % (num ,total_link, legal_name))
        os.system("youtube-dl -f 134+140 --write-sub --sub-format vtt --restrict-filenames -o "+output_sub_dir+'/'+legal_name+" "+url)
        num += 1
    print "已将所有Html文件, 找到 %d 个链接" % (len(link))

