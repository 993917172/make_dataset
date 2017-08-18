import os
import argparse as ap
import pandas as pd

if __name__ == "__main__":
    # Argument Parser
    parser = ap.ArgumentParser()
    parser.add_argument(
        "--input",
        help="Path to input files",
        default='input')
    parser.add_argument(
        "--output",
        help="Path to input files",
        default="output")
    args = vars(parser.parse_args())
    input_dir = os.path.join(args["input"], 'Proverbs')
    input_file = os.path.join(args["input"], 'text.csv')
    output_txt_dir = os.path.join(args["output"], 'txt')
    output_wav_dir = os.path.join(args["output"], 'txt')
    target_files_prefix = 'Proverbs'
    if not os.path.isdir(output_wav_dir):
        os.makedirs(output_wav_dir)
    df = pd.read_csv(input_file, names=['file_name', 'text', 'score'])
    df = df[df['file_name'].apply(lambda x: target_files_prefix in x)].reset_index(drop=True)
    print df.head()
    print(df[df.duplicated(subset=['file_name'])])
    data_len = len(df)
    data_num = 1
    for curr_line in range(data_len):
        tmp_list = list(df.ix[curr_line, :])
        tmp_file_name = tmp_list[0].split('/')[1]+'.wav'
        # if tmp_list[0].split('/')[1] != input_files[curr_line].split('.')[0]:
        #     print("find wav file and csv name mismatch!")
        #     break
        file_id = target_files_prefix+'_'+str(data_num).zfill(5)
        content = '"'+tmp_list[1]+'" \n'
        fid = open(os.path.join(output_txt_dir, file_id+'.txt'))
        fid.write(content)
        fid.close()
        if not os.path.exists(os.path.join(input_dir, tmp_file_name)):
            print("%s is not exist! Program to end~~" % (tmp_file_name))
            break
        os.system('cp '+os.path.join(input_dir, tmp_file_name)+' '+os.path.join(output_wav_dir, file_id+'.wav'))
        data_num += 1
        print("Processed: %s to %s ." % (tmp_file_name, file_id+'.wav'))
    #     if target_files_prefix in curr_line:
    #         contents = curr_line.strip().split(',')
    #         print contents
    #         break

