# 中文语音到中文音素

## import_thchs30.py
制作thchs30数据集

## import_synthesis.py
整合百度合成语音数据集

## ChineseTextToPhoneme.py
结合中文字典将中文汉字转成中文音素，保留存在字典中不存在的汉字的文本txt以便后期人工打标签
python ChineseTextToPhoneme.py --wav_dir 输入wav文件夹 --txt_dir 输入txt文件夹 --output 输出文件夹

## genChinesePhoneDict.py
根据thchs30数据集产生中文汉字对应字典(多音字会被覆盖)
python genChinesePhoneDict.py --input 输入文件夹 --output 输出文件夹

## genChineseMultiPhoneDict.py
根据thchs30数据集产生中文汉字对应字典(包含多音字列表)
python genChineseMultiPhoneDict.py --input 输入文件夹 --output 输出文件夹

## extractFailedChinese.py
根据中文文本保存字典中不存在的汉字以便扩充字典 
python extractFailedChinese.py --dict_file 输入字典文件 --txt_dir 输入txt文件夹 --output 输入文件夹为ChineseTextToPhoneme的输出fail文件夹

## Chinese_phone_dict1.json
汉字对应拼音字典(覆盖多音字)

## Chinese_phone_dict2.json
汉字对应音节字典(覆盖多音字)

## Chinese_multiphone_dict1.json
汉字对应拼音字典(包含多音字列表)

## Chinese_multiphone_dict2.json
汉字对应音节字典(包含多音字列表)

## Chinese_dict.txt
拼音对应音节字典