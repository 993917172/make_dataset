
# deepspeech.pytorch数据集制作

## (一). librivox，VoxForge，TIMIT，VCTK-Corpus数据集制作

### 1. 得到单词模型数据
分别对原始数据集解压后，修改script/文件夹下的import_librivox.py，import_voxforge.py，import_timit.py输入文件夹路径，执行在输入文件夹得到wav与txt（单词），及对应的csv文件

VCTK-Corpus数据集由script/mvDataset.py将所有wav和txt文件移动到对应两个文件夹下后，执行script/genDataCsv.py得到对应csv文件

注：上述程序得到的是单词模型需要的输入及输出

import_librivox.py需要将librivox数据集下载后自行解压后得到如下格式，如需使用clean数据集需要修改import_librivox.py，执行后会在在输入文件夹得到librivox-train-other-500.csv，librivox-dev-other.csv，librivox-dev-other.csv以及LibriSpeech文件夹下得到train-other-500-wav，train-other-500-txt，dev-other-wav, dev-other-txt，test-other-wav, test-other-txt
```
librivox-other
|-- dev-other.tar.gz
|-- LibriSpeech
|   |-- BOOKS.TXT
|   |-- CHAPTERS.TXT
|   |-- dev-other
|   |-- LICENSE.TXT
|   |-- README.TXT
|   |-- SPEAKERS.TXT
|   |-- test-other
|   |-- train-other-500
|-- test-other.tar.gz
|-- train-other-500.tar.gz
```

import_timit.py需要将timit数据集下载后自行解压后得到如下格式，执行后会在在输入文件夹得到train-wav, train-txt，test-wav, test-txt，timit-train.csv，timit-test.csv
```
timit
|-- doc
|-- readme.doc
|-- test
|-- TIMIT_phonemes.Table
|-- train
```

import_voxforge.py需要将voxforge数据集下载后自行解压，各个数据集tar压缩包在VoxForge/www.repository.voxforge1.org/downloads/SpeechCorpus/Trunk/Audio/Main/16kHz_16bit目录中，对import_voxforge.py执行：

python import_voxforge.py --input_dir ~/data/VoxForge/www.repository.voxforge1.org/downloads/SpeechCorpus/Trunk/Audio/Main/16kHz_16bit/ --target_dir voxforge --sample_rate 16000

VCTK数据集由VCTK-Corpus.tar.gz解压得到如下目录结构，对script下mvDataset.py执行：

python mvDataset.py --wav_dir  VCTK-Corpus的wav48文件夹  --txt_dir VCTK-Corpus的txt文件夹 --output_wav_dir 输出wav文件夹 --output_txt_dir 输出txt文件夹
```
VCTK-Corpus
|-- COPYING
|-- README
|-- speaker-info.txt
|-- txt
|   |-- p232
|   `-- p376等
`-- wav48
    |-- p225
    `-- p240等
```


### 2. 音素字典获取

音素字典cmudict-0.7b在script文件夹中，也可以自行下载：

① 下载英文字典[cmudict-0.7b](http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/)

② 预处理删除字典中版权说明及字典中部分存在#号注释的字符串

③ (不必要步骤) script文件夹中genPhoneSet.py可查看字典文件中音素种类及个数

### 3. 单词模型数据转换为音素模型数据

① 指定输入wav和txt文件夹及输出后，script文件夹中TextToPhoneme.py可单词模型数据转换为音素模型数据，可能存在部分数据无法转换为音素，无法全部转换成音素的txt不生成音素txt和wav,执行：

python TextToPhoneme.py --txt_dir 输入txt文件夹 --wav_dir 输入wav文件夹 --output 输出音素文件夹

程序会在输出文件夹生成phone-txt和phone-wav文件夹

② 指定转换后音素的输入wav和txt文件夹及输出后，之后执行script文件夹中genDataCsv.py得到对应csv文件

python genDataCsv.py --txt_dir 输入音素txt文件夹 --wav_dir 输入音素wav文件夹 --output_file 输出csv文件

## (二). TEB，WEB数据集制作

### 1. 准备工作
由于这两个数据集是通过程序直接得到音素模型数据，故需要执行(一)中2步骤获取音素字典文件

### 2. 得到音素模型数据
分别对原始数据集解压后，修改script文件夹下的import_TED.py，import_WEB.py输入文件夹路径，以及字典文件路径，执行在输入文件夹出输出得到wav与txt（单词），及对应的csv文件，其中WEB数据集中的文本文件text.csv调整放在WEB根目录下，各个wav文件夹在WEB目录下

### 3. 注意事项
出现找不到TextToPhoneme.py或字典文件时查看脚本的音素字典文件路径和import中TextToPhoneme.py文件路径是否正确，由于时间关系尚不支持动态指定音素字典文件

## (三) 数据集合并

### 1. 准备工作
整合由上述步骤中得到的多个csv训练文件、验证文件、测试文件，分别将需要整合的csv文件放在一个文件夹中

### 2. 程序说明
script文件夹中的merge_dataset.py和merge_dataset_directly.py是对deepspeech.pytorch/data/merge_manifests.py进行修改得到。

merge_dataset.py中在原文件选择wav持续时间的基础上增加了可以指定每个数据集取X个小时的数据的功能，少于X小时则全选，还对数据集进行乱序。

merge_dataset_directly.py则不选择wav持续时间，确认各个csv文件中wav和txt同时存在后整合到一个csv中，可选择是否计算选中数据集时间和总时间,也对数据集进行乱序。


# 使用方式

### 合并数据集文件

```
cd script/
python merge_dataset.py --output_file merged_manifest.csv --merge_dir all_manifests/ --min_duration 1 --max_duration 15 --dataset_duration -1 # durations in seconds  dataset_duration in hours
```

## 训练

```
python word_train.py --train_manifest data/train_manifest.csv --val_manifest data/val_manifest.csv --cuda --labels_path word_labels.json

python phone_train.py --train_manifest data/train_manifest.csv --val_manifest data/val_manifest.csv --cuda --labels_path phone_labels.json
```

## 测试

To evaluate a trained model on a test set (has to be in the same format as the training set):

```
python word_test.py --model_path models/deepspeech.pth.tar --test_manifest /path/to/test_manifest.csv --cuda --labels_path word_labels.json

python phone_test.py --model_path models/deepspeech.pth.tar --test_manifest /path/to/test_manifest.csv --cuda --labels_path phone_labels.json
```

## 预测

```
python word_predict.py --model_path models/deepspeech.pth.tar --audio_path /path/to/audio.wav

python phone_predict.py --model_path models/deepspeech.pth.tar --audio_path /path/to/audio.wav
```

## 其他备注

```
train常用参数：--cuda 使用GPU训练，--checkpoint 每个epoch保存一次模型，--checkpoint_per_batch X 每X个step保存一次模型，--batch_size 每次step的batch size
--continue_from X/XX.tar 从X文件夹的XX.tar缓存模型重新开始训练  --labels_path 使用的label文件

```

### Noise Augmentation/Injection

There is support for two different types of noise; noise augmentation and noise injection.

#### Noise Augmentation

Applies small changes to the tempo and gain when loading audio to increase robustness. To use, use the `--augment` flag when training.

#### Noise Injection

Dynamically adds noise into the training data to increase robustness. To use, first fill a directory up with all the noise files you want to sample from.
The dataloader will randomly pick samples from this directory.

To enable noise injection, use the `--noise_dir /path/to/noise/dir/` to specify where your noise files are. There are a few noise parameters to tweak, such as
`--noise_prob` to determine the probability that noise is added, and the `--noise_min`, `--noise_max` parameters to determine the minimum and maximum noise to add in training.

Included is a script to inject noise into an audio file to hear what different noise levels/files would sound like. Useful for curating the noise dataset.

```
python noise_inject.py --input_path /path/to/input.wav --noise_path /path/to/noise.wav --output_path /path/to/input_injected.wav --noise_level 0.5 # higher levels means more noise
```

### Checkpoints

Training supports saving checkpoints of the model to continue training from should an error occur or early termination. To enable epoch
checkpoints use:

```
python train.py --checkpoint
```

To enable checkpoints every N batches through the epoch as well as epoch saving:

```
python train.py --checkpoint --checkpoint_per_batch N # N is the number of batches to wait till saving a checkpoint at this batch.
```

Note for the batch checkpointing system to work, you cannot change the batch size when loading a checkpointed model from it's original training
run.

To continue from a checkpointed model that has been saved:

```
python train.py --continue_from models/deepspeech_checkpoint_epoch_N_iter_N.pth.tar
```

This continues from the same training state as well as recreates the visdom graph to continue from if enabled.

### Choosing batch sizes

Included is a script that can be used to benchmark whether training can occur on your hardware, and the limits on the size of the model/batch
sizes you can use. To use:

```
python benchmark.py --batch_size 32
```

Use the flag `--help` to see other parameters that can be used with the script.

### Model details

Saved models contain the metadata of their training process. To see the metadata run the below command:

```
python model.py --model_path models/deepspeech.pth.tar
```

To also note, there is no final softmax layer on the model as when trained, warp-ctc does this softmax internally. This will have to also be implemented in complex decoders if anything is built on top of the model, so take this into consideration!


### Alternate Decoders
By default, `test.py` and `predict.py` use a `GreedyDecoder` which picks the highest-likelihood output label at each timestep. Repeated and blank symbols are then filtered to give the final output.

A beam search decoder can optionally be used with the installation of the `pytorch-ctc` library as described in the Installation section. The `test` and `predict` scripts have a `--decoder` argument. To use the beam decoder, add `--decoder beam`. The beam decoder enables additional decoding parameters:
- **beam_width** how many beams to consider at each timestep
- **lm_path** optional binary KenLM language model to use for decoding
- **trie_path** trie describing lexicon. required if `lm_path` is supplied
- **lm_alpha** weight for language model
- **lm_beta1** bonus weight for words
- **lm_beta2** bonus weight for in-vocabulary words

## Acknowledgements

Thanks to [Egor](https://github.com/EgorLakomkin) and [Ryan](https://github.com/ryanleary) for their contributions!
