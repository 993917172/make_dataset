# -*- coding: utf-8 -*-
import argparse as ap
import json

if __name__ == "__main__":
    # Argument Parser
    parser = ap.ArgumentParser()
    parser.add_argument(
        "--input_file",
        help="Path to input files",
        default='cmudict-0.7b')
    parser.add_argument(
        "--output",
        help="Path to input files",
        default="output")
    args = vars(parser.parse_args())
    input_file = args["input_file"]   # input dictionary file
    lines = open(input_file).readlines()
    phone_set = set()
    for line in lines:
        line = line.replace('  ', ' ')
        line = line.strip()
        content = line.split(' ')[1:]
        for word in content:
            phone_set.add(word)
    # # phone_set = set(['AO1', 'DH', 'IH2', 'UW2', 'UW1', 'UW0', 'OY2', 'AH2', 'AH0', 'AH1', 'JH', 'UH0', 'UH1', 'OY0', 'AO0', 'EH2', 'EH0', 'EH1', 'AW2', 'NG', 'EY1', 'EY0', 'EY2', 'TH', 'AA1', 'AY1', 'IH0', 'IY0', 'B', 'ZH', 'D', 'G', 'F', 'K', 'IY2', 'M', 'L', 'AW1', 'N', 'P', 'S', 'R', 'T', 'W', 'V', 'Y', 'Z', 'OW1', 'OW0', 'OW2', 'AE1', 'AE0', 'AE2', 'ER0', 'ER1', 'ER2', 'AW0', 'CH', 'HH', 'OY1', 'AY0', 'IH1', 'SH', 'IY1', 'AA0', 'AA2', 'UH2', 'AY2', 'AO2'])
    phone_list = ['<space>']
    print len(phone_set), phone_set
    for phoneme in phone_set:
        phone_list.append(phoneme)
    phone_list.append('<stop>')
    phone_list.append('<comma>')
    phone_list.append('<question>')
    phone_list.append('<exclam>')
    phone_list.append('<semicolon>')
    phone_list.append('<colon>')
    phone_list.append('<other>')
    json.dump(phone_list, open('English_phone_set.json', 'w'), indent=4)
    # fid = file(args["input"]+'/result.json')
    # phone_list = json.load(fid)
    print phone_list
    print(type(phone_list))
    print ' '.join(phone_list)
