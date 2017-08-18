# 一、安装相关依赖

## (一)、安装htk-3.4.1
```
sudo apt-get install libx11-dev:i386
sudo apt-get install libc6-dev
sudo apt-get install libc6-dev:i386
下载htk-3.4.1，[下载链接](http://htk.eng.cam.ac.uk/download.shtml)
解压tar xvf HTK-3.4.1.tar.gz
cd htk
./configure --prefix=软件目录--exec-prefix=软件目录
如./configure --prefix=/home/hyzhan/htk --exec-prefix==/home/hyzhan/htk
make (最好不要多核编译，容易报错)
make install
```

## (二)、安装speech_tools 和festival
```
sudo apt-get install libncurses5-dev; \
wget http://festvox.org/packed/festival/2.4/festival-2.4-release.tar.gz
wget http://festvox.org/packed/festival/2.4/speech_tools-2.4-release.tar.gz
tar vxf festival-2.4-release.tar.gz;
tar vxf speech_tools-2.4-release.tar.gz
cd speech-tools
./configure --prefix=软件目录--exec-prefix=软件目录
make
make install
cd ..
cd festival
./configure --prefix=软件目录--exec-prefix=软件目录
make
make install
sudo apt-get install festival
cp -r /usr/share/festival/voices 软件目录/lib/
cp -r /usr/share/festival/dicts/ ~/festival/lib/
sudo apt-get install gawk
```

## (三)、其他依赖
```
pip install matplotlib
pip install lxml
pip install bandmat
pip install regex
pip install sklearn
pip install keras
pip install theano
```

# 二、Merlin项目调试

## （一）、项目下载及工具编译

```
git clone https://github.com/CSTR-Edinburgh/merlin.git
bash tools/compile_tools.sh
pip install -r requirements.txt
```

## （二）、align项目demo测试
```
cd merlin/misc/scripts/alignment/state_align
./setup.sh
修改config.cfg 中tools部分为之前prefix的目录，其中htk还需要再加一级目录变为xxxx/htk/HTKTools
./run_aligner.sh config.cfg

备注：之后htk出错原因涉及到找不到htk或者找不到htk/HTKTools需要在htk工具路径里添加一级目录变为xxxx/htk/HTKTools
```

## （三）、slt_arctic_demo项目测试
```
cd merlin/egs/slt_arctic/s1
./run_demo.sh
```

# 三、Merlin项目调试
```
cd merlin/egs/build_your_own_voice/s1

1.  ./01_setup.sh demo（demo为自己定义的实验名称），若命名为demo的话训练HMM模型较小，可用于测试


2. (1) 修改conf/global_settings.cfg中训练集验证集测试集的数量，不能超过wav文件总数
(2) 将wav文件夹复制到 experiments/实验名称/test_synthesis/文件夹下，建议该文件夹不要命名为wav，以免被后期生成语音覆盖，可命名为wav_origin
(3) 执行：
./02_prepare_labels.sh <path_to_wav_dir> <path_to_text_dir> <path_to_labels_dir> 
default path to wav dir(Input): database/wav 
default path to txt dir(Input): database/txt（可用cmuarctic.data格式代替） 
default path to lab dir(Output): database/labels（输出duration特征所在文件夹）
备注：若出现找不到XXX文件夹//label_state_align的话，将此处输入改为XXX文件夹，而不是XXX文件夹/

（程序运行后输出label_state_align等文件夹，并将label_state_align文件夹和file_id_list.scp复制duration_model的data文件夹下）


3.  ./03_prepare_acoustic_features.sh <path_to_wav_dir> <path_to_feat_dir>
default path to wav dir(Input): database/wav 
default path to feat dir(Output): database/feats（输出acoustic特征所在文件夹）

（程序运行后输出lf0，mgc，bap等特征文件夹，并将这些件夹和file_id_list.scp复制duration_model的data文件夹下）


4.  ./04_prepare_conf_files.sh <path_to_global_conf_file>
default path to global conf file: conf/global_settings.cfg 生成duration模型和acoustic模型的配置文件


5.  ./05_train_duration_model.sh <path_to_duration_conf_file> 
Default path to duration conf file: conf/duration_demo.conf（demo根据实验名不同而不同）
（在duration_model文件下产生gen/ inter_module/ log/ nnets_model/文件夹及在data下产生dur文件夹）

6.  ./06_train_acoustic_model.sh <path_to_acoustic_conf_file>
Default path to acoustic conf file: conf/acoustic_demo.conf
（在acoustic_model文件下产生gen/ inter_module/ log/ nnets_model/文件夹）


7.  ./07_run_merlin.sh <path_to_text_dir> <path_to_test_dur_conf_file> <path_to_test_synth_conf_file> 
default path to text dir: experiments/demo/test_synthesis/txt 
default path to test duration conf file: conf/test_dur_synth_demo.conf 
default path to test synthesis conf file: conf/test_synth_demo.conf 
（在test_synthesis下wav生成合成的wav文件，并删去中间文件）
```


# 四、遇到过的问题
1. wav对应text过短，生成.lab文件大小为0，导致训练时候报错，在制作数据集时去除wav对应text少于20个的部分，数据量较少时可以手动删除.data和.scp对应文件名
2. conf/global_settings.cfg中训练样本数超出实际wav数量
3. 执行./03_prepare_acoustic_features.sh时出现类似This function cannot support stereo file
error: The file is not .wav format.的字样，原因是制作wav数据集时输出wav文件有问题，修改ffmpeg输出wav命令后解决，应该是输出声道数的原因，还不是十分确定
4. 目前提取特征只支持16kHz和48kHz的采样率，其他采样率会报错，48kHz采样率尚未进行模型训练测试，为了不影响模型训练，制作数据时统一输出采样率为16kHz
5. 找不到speech_tools、festival、htk工具命令，自行编译源码，修改对应配置文件中工具路径后解决
