#!/usr/bin/env python
from __future__ import absolute_import, division, print_function

# Make sure we can import stuff from util/
# This script needs to be run from the root of the DeepSpeech repository
import os
import argparse
import subprocess


def update_progress(progress):
    print("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(progress * 50),
                                                  progress * 100), end="")


parser = argparse.ArgumentParser(description='Processes and downloads VoxForge dataset.')
parser.add_argument("--wav_dir", default='txt', type=str, help="Directory to store the dataset.")
parser.add_argument("--txt_dir", default='wav', type=str, help="Directory to store the dataset.")
parser.add_argument("--output", default='output/tmp', type=str, help="file path to store the csv.")
args = parser.parse_args()


if __name__ == '__main__':
    wav_dir = args.wav_dir
    txt_dir = args.txt_dir
    output_dir = args.output
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    wav_filenames = os.listdir(wav_dir)
    wav_filenames = [curr_file[:-4] for curr_file in wav_filenames]
    txt_filenames = os.listdir(txt_dir)
    txt_filenames = [curr_file[:-4] for curr_file in txt_filenames]
    filenames = list(set(wav_filenames) & set(txt_filenames))
    print(len(wav_filenames), len(txt_filenames), len(filenames))
    files = []
    duration = 0.0
    for curr_file in filenames:
        output = subprocess.check_output(['soxi -D \"%s\"' % os.path.join(wav_dir, curr_file+'.wav')], shell=True)
        duration += float(output)
        os.system('cp '+os.path.join(txt_dir, curr_file+'.txt')+' '+os.path.join(output_dir, curr_file+'.txt'))
        if duration > 3600*60:
            break
        update_progress(duration / float(3600*60))
