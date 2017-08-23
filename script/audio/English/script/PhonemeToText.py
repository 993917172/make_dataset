import os
import argparse as ap
import re


class phoneDict(object):
    def __init__(self, file_path):
        self.phone_dict = self.loadDict(file_path)

    def loadDict(self, file_path):
        fileIn = open(file_path)
        my_dict = {}
        for line in fileIn:
            lineArr = line.rstrip().split(' ')
            tmp = lineArr[1:]
            phone = ''
            for q in tmp:
                phone = phone + q
            my_dict[str(lineArr[0])] = phone
        return my_dict

    def txtToDict(self, text):
        pho_result = []
        text = text.strip().lower() 
        res = r"[^a-z]*([a-z]+)[^a-z]*"
        words = re.findall(res, text)
        original = ' '.join(words)
        targets = original.replace(' ', '  ')
        words_list = targets.split(' ')
        # print words_list
        for word in words_list:
            if word == '':
                pho_result.append(['<space>'])
            elif not self.phone_dict.has_key(str(word)):
                return -1
            else:
                pho_result.append(self.phone_dict[str(word)])
        # print((pho_result))
        return pho_result


if __name__ == "__main__":
    # Argument Parser
    parser = ap.ArgumentParser()
    parser.add_argument(
        "--input",
        help="Path to input files",
        default="input")
    parser.add_argument(
        "--output",
        help="Path to input files",
        default="output")
    args = vars(parser.parse_args())
    input_dir = os.path.join(args["input"])
    output_dir = os.path.join(args["output"])
    my_dict = phoneDict('dic.txt')
    for root, root_dir_names, root_file_names in os.walk(input_dir):
        if len(root_file_names) > 0:
            for curr_file in root_file_names:
                if curr_file.endswith('txt'):
                    lines = open(os.path.join(root, curr_file), 'r').readlines()
                    fid = open(os.path.join(output_dir, curr_file),'w')
                    curr_word = ''
                    for curr_line in lines:
                        if '<' in curr_line and curr_word != '':
                            # print curr_file, my_dict.phone_dict.keys()[my_dict.phone_dict.values().index(curr_word.strip())]
                            fid.write(my_dict.phone_dict.keys()[my_dict.phone_dict.values().index(curr_word.strip())]+' ')
                            curr_word = ''
                            if curr_line.strip() == '<space>':
                                fid.write(' ')
                            elif curr_line.strip() == '<stop>':
                                fid.write('.')
                            elif curr_line.strip() == '<comma>':
                                fid.write(',')
                            elif curr_line.strip() == '<question>':
                                fid.write('?')
                            elif curr_line.strip() == '<exclam>':
                                fid.write('!')
                            elif curr_line.strip() == '<semicolon>':
                                fid.write(';')
                            elif curr_line.strip() == '<colon>':
                                fid.write(':')
                            else:
                                fid.write(' ')
                        else:
                            curr_word += curr_line.strip()
                    fid.write('\n')
                    fid.close()


