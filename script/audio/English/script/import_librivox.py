#!/usr/bin/env python
from __future__ import absolute_import, division, print_function

# Make sure we can import stuff from util/
# This script needs to be run from the root of the DeepSpeech repository
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import codecs
import fnmatch
import pandas
import unicodedata


def _preprocess_data(data_dir):

    print("Converting FLAC to WAV and splitting transcriptions...")
    LIBRIVOX_DIR = "LibriSpeech"
    work_dir = os.path.join(data_dir, LIBRIVOX_DIR)
    # train_100 = _convert_audio_and_split_sentences(work_dir, "train-clean-100", "train-clean-100-wav")
    # train_360 = _convert_audio_and_split_sentences(work_dir, "train-clean-360", "train-clean-360-wav")
    train_500 = _convert_audio_and_split_sentences(work_dir, "train-other-500", "train-other-500-wav", "train-other-500-txt")
    # dev_clean = _convert_audio_and_split_sentences(work_dir, "dev-clean", "dev-clean-wav")
    dev_other = _convert_audio_and_split_sentences(work_dir, "dev-other", "dev-other-wav", "dev-other-txt")
    # test_clean = _convert_audio_and_split_sentences(work_dir, "test-clean", "test-clean-wav")
    test_other = _convert_audio_and_split_sentences(work_dir, "test-other", "test-other-wav", "test-other-txt")

    # Write sets to disk as CSV files
    # train_100.to_csv(os.path.join(data_dir, "librivox-train-clean-100.csv"), index=False)
    # train_360.to_csv(os.path.join(data_dir, "librivox-train-clean-360.csv"), index=False)
    train_500.to_csv(os.path.join(data_dir, "librivox-train-other-500.csv"), index=False, header=False)

    # dev_clean.to_csv(os.path.join(data_dir, "librivox-dev-clean.csv"), index=False)
    dev_other.to_csv(os.path.join(data_dir, "librivox-dev-other.csv"), index=False, header=False)

    # test_clean.to_csv(os.path.join(data_dir, "librivox-test-clean.csv"), index=False)
    test_other.to_csv(os.path.join(data_dir, "librivox-test-other.csv"), index=False, header=False)


def _convert_audio_and_split_sentences(extracted_dir, data_set, dest_dir, dest_dir2):
    source_dir = os.path.join(extracted_dir, data_set)
    target_dir = os.path.join(extracted_dir, dest_dir)
    target_txt_dir = os.path.join(extracted_dir, dest_dir2)

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    if not os.path.exists(target_txt_dir):
        os.makedirs(target_txt_dir)

    files = []
    for root, dirnames, filenames in os.walk(source_dir):
        print(root, dirnames, len(filenames))
        for filename in fnmatch.filter(filenames, '*.trans.txt'):
            trans_filename = os.path.join(root, filename)
            with codecs.open(trans_filename, "r", "utf-8") as fin:
                for line in fin:
                    # Parse each segment line
                    first_space = line.find(" ")
                    seqid, transcript = line[:first_space], line[first_space+1:]

                    # We need to do the encode-decode dance here because encode
                    # returns a bytes() object on Python 3, and text_to_char_array
                    # expects a string.
                    transcript = unicodedata.normalize("NFKD", transcript)  \
                                            .encode("ascii", "ignore")      \
                                            .decode("ascii", "ignore")

                    transcript = transcript.lower().strip()
                    if '"' in transcript:
                        transcript = transcript.replace('"', '')
                    # print(transcript)
                    txt_file = os.path.join(target_txt_dir, seqid+".txt")
                    txt_fid = open(txt_file, 'w')
                    txt_fid.write(transcript+'\n')
                    txt_fid.close()

                    # Convert corresponding FLAC to a WAV
                    flac_file = os.path.join(root, seqid + ".flac")
                    wav_file = os.path.join(target_dir, seqid + ".wav")
                    if not os.path.exists(wav_file):
                        os.system('sox '+flac_file+' '+wav_file)
                    # wav_filesize = os.path.getsize(wav_file)

                    files.append((os.path.abspath(wav_file), os.path.abspath(txt_file)))

    return pandas.DataFrame(data=files, columns=["wav_filename", "txt_filename"])


if __name__ == "__main__":
    _preprocess_data('/data5/hyzhan/data/librivox-other')

# librivox-other
# |-- dev-other.tar.gz
# |-- LibriSpeech
# |   |-- BOOKS.TXT
# |   |-- CHAPTERS.TXT
# |   |-- dev-other
# |   |-- LICENSE.TXT
# |   |-- README.TXT
# |   |-- SPEAKERS.TXT
# |   |-- test-other
# |   |-- train-other-500
# |-- test-other.tar.gz
# |-- train-other-500.tar.gz

