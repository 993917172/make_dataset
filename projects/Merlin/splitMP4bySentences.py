# -*- coding: utf-8 -*-
import os
import argparse as ap
import re

def my_timeSub(start_time, end_time):
    [h1, m1, s1] = [int(i) for i in start_time.split('.')[0].split(':')]
    w1 = int(start_time.split('.')[1])
    [h2, m2, s2] = [int(i) for i in end_time.split('.')[0].split(':')]
    w2 = int(end_time.split('.')[1])
    diff = (h2 - h1) * 3600 * 1000 + (m2 - m1) * \
        60 * 1000 + (s2 - s1) * 1000 + (w2 - w1)
    h3 = diff / (3600*1000)
    m3 = diff % (3600*1000) / (60*1000)
    s3 = diff %(60*1000) / 1000
    w4 = diff % 1000
    return str(h3).zfill(2)+':'+str(m3).zfill(2)+':'+str(s3).zfill(2)+'.'+str(w4).zfill(3)


if __name__ == "__main__":
    # Argument Parser
    parser = ap.ArgumentParser()
    parser.add_argument(
        "--input",
        help="Path to input video files default = /../data/mp4/",
        required=True)
    parser.add_argument(
        "--output",
        help="Path to output wav files default = /../data/origin2/",
        default='output')
    parser.add_argument(
        "--output_name",
        help="Path to output pepole",
        required=True)
    parser.add_argument(
        "--pass",
        help="Ignore every mp4 file first DEL num audio",
        default=1)
    args = vars(parser.parse_args())
    input_dir = os.path.join(os.getcwd(), args["input"])
    output_dir = os.path.join(os.getcwd(), args["output"])
    output_name = args["output_name"]
    output_work_dir = os.path.join(output_dir, output_name)
    output_wav_dir = os.path.join(output_work_dir, 'wav_origin')
    output_tmp_wav_dir = os.path.join(output_work_dir, 'wav_mp4')
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    if os.path.isdir(output_work_dir):
        os.system("rm -r "+output_work_dir)
        os.mkdir(output_work_dir)
    else:
        os.mkdir(output_work_dir)
    if not os.path.isdir(output_wav_dir):
        os.mkdir(output_wav_dir)
    if not os.path.isdir(output_tmp_wav_dir):
        os.mkdir(output_tmp_wav_dir)
    print input_dir
    print "开始处理MP4文件"
    output_num = 1
    total_time = 0
    output_time = 0
    cmu_data = open(os.path.join(output_work_dir, "cmuarctic.data"), mode='w')
    file_id_list = open(os.path.join(output_work_dir, "file_id_list.scp"), mode='w')
    text_txt = open(os.path.join(output_work_dir, output_name+".txt"), mode='w')
    for root, root_dir_names, root_file_names in os.walk(input_dir):
        print root, root_dir_names, len(root_file_names)
        if len(root_file_names) == 2:
            for file_name in root_file_names:
                if not file_name.endswith('mp4'):
                    srt_file = file_name
                else:
                    target_file = os.path.join(root, file_name)
            output_file_dir = file_name.split('.')[0]
            output_file_path = os.path.join(
                output_tmp_wav_dir, output_file_dir + ".wav")
            print(target_file, output_file_path)
            # os.system("ffmpeg -i "+"'" + target_file + "'" + " -vn -ac 2 -y " + output_file_path)
            os.system("ffmpeg -i "+"'" + target_file + "'" + " -vn -v quiet -ac 2 -y " + output_file_path)
            target_file_length_str = os.popen("ffmpeg -i "+output_file_path+" 2>&1 | grep 'Duration' | cut -d ' ' -f 4 | sed s/,//").readlines()
            target_file_length_list = target_file_length_str[0].strip().split(':')
            target_file_length = int(float(target_file_length_list[0])*3600+float(target_file_length_list[1])*60+float(target_file_length_list[2]))
            total_time += target_file_length
            print(" %s last time: %d" % (target_file, target_file_length))
            f = open(os.path.join(root, srt_file), mode='r')
            lines = f.readlines()
            data_len = len(lines)
            pass_num = int(args["pass"])
            mp4_tail = data_len - 4 * pass_num - 2
            target_file = output_file_path
            for index in range(data_len-1):
                if index > mp4_tail:
                    break
                line = lines[index]
                if '-->' in line:
                    if pass_num > 0:
                        pass_num -= 1
                        continue
                    next_line = lines[index+1].strip()
                    index += 1
                    while len(lines[index+1].strip()) > 3:
                        next_line = next_line+' '+lines[index+1].strip()
                        index += 1
                    if '&' in next_line or '%' in next_line or '$' in next_line:
                        continue
                    if len(re.findall(r"\d+", next_line)) > 0:
                        continue
                    res = r"^\s*[A-Z]+.+\.\s*$"
                    if len(re.findall(res, next_line)) == 0:
                        continue
                    if '-' in next_line:
                        next_line = next_line.replace('-',' ')
                    line = line.strip().split('-->')
                    start_time = line[0].strip()
                    end_time = line[-1].strip()
                    file_id = output_name+'_'+str(output_num).zfill(5)
                    output_file_path = os.path.join(output_wav_dir, file_id+'.wav')
                    last_time = my_timeSub(start_time, end_time)
                    print(output_file_path, next_line, start_time, last_time, end_time)
                    # os.system("ffmpeg -ss "+start_time+" -i "+target_file+" -t "+last_time+" -ac 1 -ar 16000 -y "+output_file_path)
                    os.system("ffmpeg -ss "+start_time+" -i "+target_file+" -t "+last_time+" -v quiet -ac 1 -ar 16000 -y "+output_file_path)
                    output_time += int(last_time.split('.')[0].split(':')[2])
                    next_line = next_line.replace('-', '')
                    content = '( '+file_id+' "'+next_line.strip()+'" )\n'
                    cmu_data.write(content)
                    file_id_list.write(file_id+'\n')
                    text_txt.write(srt_file+' '+file_id+' '+next_line+'\n')
                    output_num += 1
            print "已处理完 %s 下MP4文件" % (root)
            print("生成最后一个文件为: %s " % (file_id))

    print "已将所有MP4文件转换成wav文件"
    os.system("touch "+str(output_num)+"_file_"+str(output_time)+"_seconds.txt")
    print("wav总时长: %d 秒, %d 分, 训练总时长: %d 秒, %d 分" % (total_time, total_time/60, output_time, output_time/60))
    cmu_data.close()
    file_id_list.close()
    text_txt.close()


