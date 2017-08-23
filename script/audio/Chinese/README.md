## (一). thchs30数据集制作

### 整合转换数据
分别对原始数据集解压后，修改script/文件夹下的import_thcs30.py，输入文件夹路径，执行在输入文件夹得到wav与txt（汉字），及对应的csv文件
import_thcs30.py文件中的target_line参数默认为3，输出音节txt，等于2时输出拼音txt
```
thchs30
|-- data
|-- dev
|-- lm_phone
|-- lm_word
|-- README.TXT
|-- test
`-- train
```
执行后文件目录：
```
.
├── data
├── dev
├── dev-2-txt   验证集拼音txt文件
├── dev-3-txt   验证集音节txt文件
├── dev-wav     验证集wav文件
├── lm_phone
├── lm_word
├── README.TXT
├── test
├── test-2-txt  测试集拼音txt文件
├── test-3-txt  测试集音节txt文件
├── test-wav    测试集wav文件
├── thchs30-dev-2.csv   验证集wav文件路径与拼音txt文件路径
├── thchs30-dev-3.csv   验证集wav文件路径与音节txt文件路径
├── thchs30_phone_2.json  thchs30 deepspeech.pytorch用拼音label文件
├── thchs30_phone_3.json  thchs30 deepspeech.pytorch用音节label文件
├── thchs30-test-2.csv  测试集wav文件路径与拼音txt文件路径
├── thchs30-test-3.csv  测试集wav文件路径与音节txt文件路径
├── thchs30-train-2.csv  训练集wav文件路径与拼音txt文件路径
├── thchs30-train-3.csv  训练集wav文件路径与音节txt文件路径
├── train
├── train-2-txt  训练集拼音txt文件
├── train-3-txt  训练集音节txt文件
└── train-wav    训练集wav文件
```
拼音txt文件格式：
```
ben2
<space>
ban3
<space>
yi1
<space>
yi1
<space>
jiu3
<space>
er4
<space>
```

音节txt文件格式：
```
b
en2
<space>
b
an3
<space>
ii
i1
<space>
ii
i1
<space>
j
iu3
<space>
ee
er4
<space>
```

### 原始字典产生
script/genChineseMultiPhoneDict.py
根据thcs30数据中的data文件夹生成原始多音字字典，以及拼音到音节的字典

python genChineseMultiPhoneDict.py --input thcs30数据中的data文件夹 --output 输出文件夹

输出得到原始拼音音节字典：Chinese_phone2phone_dict.json
得到原始汉字拼音字典：Chinese_multiphone_dict1.json
得到原始汉字音节字典：Chinese_multiphone_dict2.json

## (二). 百度合成数据集制作

### 1. 整合转换数据
分别对合成数据集解压后，修改script/文件夹下的import_synthesis.py，输入文件夹路径，执行在输入文件夹得到synthesis-wav与synthesis-txt（汉字），及对应的csv文件，其中由于下载问题synthesis-wav和synthesis-txt数量可能不一致，以csv文件中记录文件为准，synthesis下文件夹名称若存在空格会出现错误，建议重新命名后执行脚本。修改内容：

_preprocess_data(输入文件夹路径, 输出文件夹路径)

```
synthesis
|-- 【丹】安徒生：安徒生童话.txt
        |-- 0.mp3
        |-- 0.txt
        |-- 100.mp3
        |-- 100.txt
        等等

|-- 【俄】列夫·托尔斯泰：复活.txt
等待
```
执行脚本后目录结构：
```
synthesis（可能为其他名称）
|-- synthesis.csv  （可能为其他名称）
|-- synthesis-txt   百度合成txt
|-- synthesis-wav   百度合成wav
synthesis-txt 格式如下：
"陛下，臣恳求您。"
```

### 2. 汉字模型数据转换为音素模型数据

指定输入wav和txt文件夹及输出后，script文件夹中ChineseTextToPhoneme.py可单词模型数据转换为音素模型数据，能全部转换成音素的输出音素txt到output文件夹phone-txt文件夹下，可能存在部分数据无法转换为音素，无法全部转换成音素的txt将输出到failed-txt,执行：

python ChineseTextToPhoneme.py --txt_dir 输入txt文件夹 --dict_file 字典文件 --output 输出音素文件夹

字典文件位于项目script/Chinese_5000.json, 程序会在输出文件夹生成phone-txt和phone-wav文件夹

如输入上述synthesis文件夹后，执行结果如下：
```
synthesis
|-- failed-txt
|-- phone-txt
|-- synthesis.csv
|-- synthesis-txt
|-- synthesis-wav
```
failed-txt文件格式如下：
```
“那就给我吧。”
<quotation> n a4 j iu4 <multi> <multi> <unfound> <stop> <quotation>
给我吧
g ei2 g ei3 j i2,uu uo2 uu uo3,#

第一行为原始文本，第二行为转换后音素，<multi>表示这个位置的汉字为多音字，<unfound>表示字典中不存在该汉字
第三行为多音字或者是不存在的汉字，第四行为多音字对应多个发音的音节，#表示不存在的汉字

phone-txt格式如下：
<quotation>
<space>
n i3
<space>
sh ou4
<space>
sh ang1
<space>
l a5
<space>
<question>
<space>
<quotation>
<space>
其中n i3部分空格未分开，后续需进一步处理才能用于训练
```

### 3. 转换音素失败txt处理(一)
script文件夹中MissTxtToFixTxt.py能将failed-txt中的txt转换成竖直排列的txt，方便人工打标签，执行：

python MissTxtToFixTxt.py --txt_dir 输入txt文件夹 --dict_file 字典文件 --output 输出文件夹

转换后的文件在output文件夹fix-failed-txt文件夹下

failed-txt文件转换为fix-failed-txt文件格式如下：
```
你 n i3
就 j iu4
不 ###b u2,b u5,b u4
能 n eng2
帮 b ang1
我 ###uu uo2,uu uo3
找 zh ao3
找 zh ao3
那 n a4
只 ###zh ix1,zh ix3,zh ix2
两 ###l iang2,l iang3
毛 m ao2
五 ###uu u2,uu u3
的 ###d i2,d e5,d i4
镚 @@@
子 ###z iy5,z iy3
儿 ###ee er2,ee er5
， <comma>
好 ###h ao3,h ao2,h ao4
让 r ang4
我 ###uu uo2,uu uo3
今 j in1
儿 ###ee er2,ee er5
晚 uu uan3
上 ###sh ang4,sh ang5
去 ###q v5,q v4
看 ###k an5,k an4,k an1
演 ii ian3
出 ch u1
。 <stop>
" <quotation>

@@@表示字典中不存在的汉字，###表示多音字，加上###和@@@主要是方便人工打标签时能快速定位到需要标记的区域，提高注意力
```

### 4. 转换人工打标签后txt为音素txt
执行script文件夹中 mergeHumanMark.py：

python mergeHumanMark.py --input 输入fix-failed-txt文件夹 --output 输出音素文件夹

转换后的文件在output文件夹fix-failed-txt文件夹下
```
输入打标签后fix-failed-txt文件格式：
“ <quotation>
我 uu uo3
怎 z en3
么 m e5
知 zh ix1
道 d ao4
呢 n e5
？ <question>
” <quotation>


输出文件格式
<quotation>
<space>
uu uo3
<space>
z en3
<space>
m e5
<space>
zh ix1
<space>
d ao4
<space>
n e5
<space>
<question>
<space>
<quotation>
<space>
与ChineseTextToPhoneme.py生成的phone-txt相同
```

### 4.5 转换音素txt问题修正
由于ChineseTextToPhoneme.py生成的phone-txt中每一行声母韵母之间还存在，训练时会报错，执行script/fixLabelBug.py修正这个问题，将上述fix-failed-txt文件夹中txt复制到ChineseTextToPhoneme.py中phone-txt中，

python fixLabelBug.py --input 输入声母韵母之间存在空格的txt文件夹 --output 修改后输出txt文件夹

输出文件格式：
```
uu
uo3
<space>
h
en2
<space>
j
iu3
<space>
m
ei2
<space>
d
ao4
<space>
```

### 5. 整合音素数据
之后执行script文件夹中 genDataCsv.py得到对应csv文件

python genDataCsv.py --txt_dir 输入音素txt文件夹 --wav_dir 输入音素wav文件夹 --output_file 输出csv文件

### 6. 转换音素失败txt处理(二)
执行script文件夹中extractFailedChinese.py：

python extractFailedChinese.py --txt_dir 输入failed-txt文件夹 --dict_file 字典文件 --output 输出文件夹

在output文件夹生成expand_words.txt为字典中不存在的汉字，每个汉字一行，后期人工补充字典格式为：汉字 拼音:声母 韵母(,拼音:声母 韵母)，
单音字不存在括号部分。
expand_words.txt文件格式为：
```
吧
鹏
霍
狱
扇
盯
摸
伙
剔
怜
```
补充方式需要的脚本：script/genChineseMultiPhoneDict.py
根据thcs30数据中的data文件夹生成原始多音字字典，以及拼音到音节的字典

python genChineseMultiPhoneDict.py --input thcs30数据中的data文件夹 --output 输出文件夹

输出得到拼音音节字典：Chinese_phone2phone_dict.json，对于每个不存在的汉字在网上查询实际发音，若发音在Chinese_phone2phone_dict.json存在则对照该文件进行标注，Chinese_phone2phone_dict.json也不存在的拼音，商量后自定义字典补充，打完标签后文件见下一步骤。

### 7. 字典扩充合并文本
执行script文件夹中expandDictionary.py：
python extractFailedChinese.py --mark_dir 人工补充字典txt文件夹 --dict_file 字典文件 --expand_type 补充字典类型pinyin或者其他 --output_file 输出新字典文件名
```
输入文件格式（多音字用逗号分隔，拼音和音节用冒号分隔，音节本身用空格分隔）：
吧 ba4:b a4,ba5:b a5
鹏 peng2:p eng2
霍 huo4:h uo4
狱 yu4:vv v4
扇 shan1:sh an1,shan4:sh an4
盯 ding1:d ing1
摸 mo1:m o1
伙 huo3:h uo3,huo5:h uo5
剔 ti1:t i1
怜 lian2:l ian2

输出文件格式与原字典相同，为汉字对应发音列表字典。
```

### 8. 字典文件到deepspeech.pytorch标签文件
脚本script/ChineseDictToLabel.py用于生成deepspeech.pytorch标签文件

python ChineseDictToLabel.py --dict_file 字典文件 --label_file 生成label文件

生成文件格式:
```
[
    "_", 
    "a1", 
    "a2", 
    "a3", 
    "a4", 
    省略部分,
    "zh", 
    "<stop>", 
    "<exclam>", 
    "<pause>", 
    "<quotation>", 
    "<question>", 
    "<comma>", 
    "<colon>", 
    "<semicolon>", 
    "<space>"
]
```

## (二) 数据集合并

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
