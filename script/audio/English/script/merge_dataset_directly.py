from __future__ import print_function
import argparse
import io
import os
import traceback
import subprocess
import random


def update_progress(progress):
    print("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(progress * 50),
                                                  progress * 100), end="")


parser = argparse.ArgumentParser(description='Merges all manifest CSV files in specified folder.')
parser.add_argument('--merge_dir', default='manifests/', help='Path to all manifest files you want to merge')
parser.add_argument('--output_file', default='merged_manifest.csv', help='Output path to merged manifest')
parser.add_argument('--cal_time', default='False', type=bool, help='Output path to merged manifest')

args = parser.parse_args()

dataset_files = []
dataset_names = []
for file in os.listdir(args.merge_dir):
    if file.endswith(".csv"):
        dataset_names.append(file)
        files = []
        with open(os.path.join(args.merge_dir, file), 'r') as fh:
            files += fh.readlines()
        dataset_files.append(files)

new_files = []
dataset_size = len(dataset_files)
# print(len(dataset_files))
total_duration = 0.0
for i in range(dataset_size):
    files = dataset_files[i]
    size = len(files)
    curr_dataset_duration = 0.0
    print(size)
    print("Processing dataset: %s" % (dataset_names[i]))
    for x in range(size):
        file_path = files[x]
        wav_path = file_path.split(',')[0].strip()
        txt_path = file_path.split(',')[1].strip()
        # print(wav_path, txt_path)
        # print(os.path.exists(wav_path) and os.path.exists(txt_path))
        # new_files.append(files[x])
        # if os.path.exists(wav_path):
        if os.path.exists(wav_path) and os.path.exists(txt_path):
            new_files.append(files[x])
        else:
            continue
        if args.cal_time:
            try:
                output = subprocess.check_output(
                    ['soxi -D \"%s\"' % wav_path.strip()],
                    shell=True
                )
            except:
                traceback.print_exc()
                continue
            duration = float(output)
            total_duration += duration
            curr_dataset_duration += duration
        update_progress(x / float(size))
    if args.cal_time:
        print("\ndataset_duration: %.3f " % (curr_dataset_duration))
if args.cal_time:
    print("total_duration: %.3f " % (total_duration))
# print("\nSorting files by length...")
# def func(element):
#     return element[1]
# new_files.sort(key=func)

print("\nShuffling files...")
random.shuffle(new_files)

print("Saving new manifest...")

with io.FileIO(args.output_file, 'w') as f:
    for file_path in new_files:
        sample = file_path.strip() + '\n'
        f.write(sample.encode('utf-8'))
