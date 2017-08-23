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
parser.add_argument('--min_duration', default=-1, type=int,
                    help='Optionally prunes any samples shorter than the min duration (given in seconds, default off)')
parser.add_argument('--max_duration', default=-1, type=int,
                    help='Optionally prunes any samples longer than the max duration (given in seconds, default off)')
parser.add_argument('--dataset_duration', default=-1, type=int,
                    help='Optionally prunes any samples longer than the dataset_duration (given in hours, default off)')
parser.add_argument('--output_file', default='merged_manifest.csv', help='Output path to merged manifest')

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
prune_min = args.min_duration >= 0
prune_max = args.max_duration >= 0
if prune_min:
    print("Pruning files with minimum duration %d" % (args.min_duration))
if prune_max:
    print("Pruning files with  maximum duration of %d" % (args.max_duration))

new_files = []
dataset_size = len(dataset_files)
# print(len(dataset_files))
total_duration = 0.0
for i in range(dataset_size):
    files = dataset_files[i]
    size = len(files)
    curr_dataset_duration = 0.0
    # print(size)
    print("Processing dataset: %s" % (dataset_names[i]))
    for x in range(size):
        file_path = files[x]
        file_path = file_path.split(',')[0]
        try:
            output = subprocess.check_output(
                ['soxi -D \"%s\"' % file_path.strip()],
                shell=True
            )
        except:
            traceback.print_exc()
            continue
        duration = float(output)
        if prune_min or prune_max:
            duration_fit = True
            if prune_min:
                if duration < args.min_duration:
                    duration_fit = False
            if prune_max:
                if duration > args.max_duration:
                    duration_fit = False
            if duration_fit:
                new_files.append((files[x], duration))
                total_duration += duration
                curr_dataset_duration += duration
        else:
            new_files.append((files[x], duration))
        prune_dataset = args.dataset_duration > 0
        if prune_dataset:
            update_progress(curr_dataset_duration / float(args.dataset_duration*3600))
            if curr_dataset_duration > args.dataset_duration*3600:
                print("\ndataset: %s reach %d hours " % (dataset_names[i], args.dataset_duration))
                break
        else:
            update_progress(x / float(size))
    print("\ndataset_duration: %.3f " % (curr_dataset_duration))
    print('\n')
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
        sample = file_path[0].strip() + '\n'
        f.write(sample.encode('utf-8'))
