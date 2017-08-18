# 语音到语音

## genDataCsv.py 产生wav-txt对应路径csv文件
python genDataCsv.py --wav_dir 输入wav文件夹 --txt_dir 输入txt文件夹 --output_file 输出csv文件名


## merge_dataset.py 合并数据集文件，在原文件选择wav持续时间的基础上增加了可以指定每个数据集取X个小时的数据的功能，少于X小时则全选，还对数据集进行乱序。
python merge_dataset.py --output_file merged_manifest.csv --merge_dir all_manifests/ --min_duration 1 --max_duration 15 --dataset_duration -1 # durations in seconds  dataset_duration in hours

## merge_dataset.py 则不选择wav持续时间，确认各个csv文件中wav和txt同时存在后整合到一个csv中，可选择是否计算选中数据集时间和总时间,也对数据集进行乱序。
python merge_dataset_directly.py --output_file merged_manifest.csv --merge_dir all_manifests/  --cal_time False # default not to cal time

## mvDataset.py 递归移动wav和txt文件
python genDataCsv.py --wav_dir 输入wav文件夹 --txt_dir 输入txt文件夹 --output_wav_dir 输出wav文件夹 --output_txt_dir 输出txt文件夹
