# -*- coding: utf-8 -*-
import numpy as np
from os.path import join, isfile

dict_filename = r'D:\Users\Administrator\Desktop\dic.txt'

def loadDict():
    fileIn = open(dict_filename)
    my_dict = {}
    for line in fileIn:
        lineArr = line.rstrip().split(' ')
        tmp = lineArr[1:]
        phone = ''
        for q in tmp:
            phone = phone + q
        my_dict[str(lineArr[0])] = phone
    return my_dict


def txtToDict(text):
    my_dict = loadDict()
    x = my_dict.keys()[my_dict.values().index(text)]
    return x


if __name__ == '__main__':
    file = r'D:\Users\Administrator\Desktop\test.txt'
    with open(file, 'r') as f1:
        txt = f1.readlines()
    y = [i for i, v in enumerate(txt) if (v == '<space>\n') | (v == '<exclam>\n')]
    setence = ''
    for i in range(len(y)):
        if i == 0:
            star = 0
        else:
            star = y[i - 1] + 1
        end = y[i]
        tmp_index = txt[star:end]
        single_phone = ''
        for j in tmp_index:
            single_phone = single_phone + j.strip()
        z = txtToDict(single_phone)
        setence = setence + z + ' '
    print setence