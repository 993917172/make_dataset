# -*- coding: utf-8 -*-
import os
import fnmatch
import argparse as ap
import time
from multiprocessing import Pool as mp
from aip import AipSpeech


APP_ID = '8064450'
API_KEY = '3OpMM1ACnho8pT4tXnNLGbYy'
SECRET_KEY = 'ef43f26fd00a6e178b7ea6917b1e8864'


def synthesis(text, PERSON=3, SPEED=4):
    # 初始化AipSpeech对象
    aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = aipSpeech.synthesis(text, 'zh', 1, {
        'per': PERSON,
        'spd': SPEED
    })
    return result


def write_audio(data, output_path):
    # 识别正确返回语音二进制，错误则返回dict 参照下面错误码
    if not isinstance(data, dict):
        # wav.write(output_path, 16000, data)
        with open(output_path, 'wb') as f:
            f.write(data)
    else:
        print("error dict:", data)


def write_text(data, output_path):
    # 识别正确返回语音二进制，错误则返回dict 参照下面错误码
    with open(output_path, 'wb') as f:
        f.write(data)


def main(text, output_wav_path, output_txt_path):
    result = synthesis(text)
    write_text(text, output_txt_path)
    time.sleep(1)
    write_audio(result, output_wav_path)
    time.sleep(5)
    

if __name__ == "__main__":
    # Argument Parser
    parser = ap.ArgumentParser()
    parser.add_argument(
        "--input",
        help="Path to input video files default = /../data/mp4/",
        default='output2/least')
        # required=True)
    parser.add_argument(
        "--output",
        help="Path to output wav files default = /../data/origin2/",
        default='output')
    args = vars(parser.parse_args())
    input_dir = os.path.join(os.getcwd(), args["input"])
    output_dir = os.path.join(os.getcwd(), args["output"])
    output_wav_dir = os.path.join(output_dir, 'wav')
    output_txt_dir = os.path.join(output_dir, 'txt')
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    if not os.path.isdir(output_wav_dir):
        os.makedirs(output_wav_dir)
    if not os.path.isdir(output_txt_dir):
        os.makedirs(output_txt_dir)

    print input_dir
    file_num = 0
    processers = mp(8)
    for root, root_dir_names, root_file_names in os.walk(input_dir):
        # print root, root_dir_names, len(root_file_names)
        for filename in fnmatch.filter(root_file_names, '*.txt'):
            print("Processing: %s " % (filename.decode('gbk')))
            file_path = os.path.join(root, filename)
            try:
                fin = open(file_path, 'r')
                lines = fin.readlines()
                fin.close()
            except:
                print("Failed open %s" % (filename.decode('gbk')))
                continue
            output_wav_dir = os.path.join(output_dir, filename, 'wav')
            output_txt_dir = os.path.join(output_dir, filename, 'txt')
            if not os.path.isdir(output_wav_dir):
                os.makedirs(output_wav_dir)
            if not os.path.isdir(output_txt_dir):
                os.makedirs(output_txt_dir)
            for line in lines:
                file_num += 1
                output_wav_path = os.path.join(output_wav_dir, str(file_num).zfill(7)+'.mp3')
                output_txt_path = os.path.join(output_txt_dir, str(file_num).zfill(7)+'.txt')
                # print(output_txt_path, line.decode('utf-8'), file_num)
                print(str(file_num).zfill(7))
                processers.apply_async(main, args=(line, output_wav_path, output_txt_path))
                # time.sleep(1)
    processers.close()
    processers.join()
    print("synthesised %d files" % (file_num))
