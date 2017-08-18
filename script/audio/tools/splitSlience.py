#!/usr/bin/env python
from scipy.io import wavfile
import os
import numpy as np
import argparse
from tqdm import tqdm
import fnmatch


def windows(signal, window_size, step_size):
    if type(window_size) is not int:
        raise AttributeError("Window size must be an integer.")
    if type(step_size) is not int:
        raise AttributeError("Step size must be an integer.")
    for i_start in xrange(0, len(signal), step_size):
        i_end = i_start + window_size
        if i_end >= len(signal):
            break
        yield signal[i_start:i_end]


def energy(samples):
    return np.sum(np.power(samples, 2.)) / float(len(samples))


def rising_edges(binary_signal):
    previous_value = 0
    index = 0
    for x in binary_signal:
        if x and not previous_value:
            yield index
        previous_value = x
        index += 1


def convertTime(sample_num, sample_rate):
    seconds = sample_num/float(sample_rate)
    minute = int(seconds) / 60
    second = int(seconds) % 60
    millisecond = int(seconds * 100 % 100)
    return str(minute).zfill(2)+str(second).zfill(2)+str(millisecond).zfill(2)
# Process command line arguments


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split a WAV file at silence.')
    parser.add_argument('--input_dir', type=str, default='input', help='The WAV file to split.')
    parser.add_argument('--output_dir', '-o', type=str, default='output', help='The output folder. Defaults to the current folder.')
    parser.add_argument('--min_silence_length', '-m', type=float, default=0.2, help='The minimum length of silence at which a split may occur [seconds]. Defaults to 3 seconds.')
    parser.add_argument('--silence_threshold', '-t', type=float, default=1e-6, help='The energy level (between 0.0 and 1.0) below which the signal is regarded as silent. Defaults to 1e-6 == 0.0001%.')
    parser.add_argument('--step-duration', '-s', type=float, default=None, help='The amount of time to step forward in the input file after calculating energy. Smaller value = slower, but more accurate silence detection. Larger value = faster, but might miss some split opportunities. Defaults to (min-silence-length / 10.).')
    parser.add_argument('--dry_run', '-n', action='store_true', help='Don\'t actually write any output files.')
    args = parser.parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    
    window_duration = args.min_silence_length
    if args.step_duration is None:
        step_duration = window_duration / 10.
    else:
        step_duration = args.step_duration
    silence_threshold = args.silence_threshold
    dry_run = args.dry_run

    for root, root_dir_names, root_file_names in os.walk(input_dir):
        print root, root_dir_names, len(root_file_names)
        for input_filename in fnmatch.filter(root_file_names, '*.mp3'):
            print("Converting {} to {}".format(input_filename, input_filename[:-4]+'.wav'))
            wav_filename = os.path.join(root, input_filename[:-4]+'.wav')
            mp3_filename = os.path.join(root, input_filename)
            if not os.path.exists(wav_filename):
                os.system('sox '+mp3_filename+' -b 16 -r 16000 '+wav_filename)
            input_filename = input_filename[:-4]+'.wav' 
            print "Splitting {} where energy is below {}% for longer than {}s.".format(
                input_filename,
                silence_threshold * 100.,
                window_duration
            )
            # Read and split the file
            output_filename_prefix = os.path.splitext(os.path.basename(input_filename))[0]
            sample_rate, samples = input_data = wavfile.read(filename=os.path.join(root, input_filename), mmap=True)
            max_amplitude = np.iinfo(samples.dtype).max
            max_energy = energy([max_amplitude])
            window_size = int(window_duration * sample_rate)
            step_size = int(step_duration * sample_rate)
            signal_windows = windows(
                signal=samples,
                window_size=window_size,
                step_size=step_size
            )
            window_energy = (energy(w) / max_energy for w in tqdm(
                signal_windows,
                total=int(len(samples) / float(step_size))
            ))

            window_silence = (e > silence_threshold for e in window_energy)

            cut_times = (r * step_duration for r in rising_edges(window_silence))
            # This is the step that takes long, since we force the generators to run.
            print "Finding silences..."
            cut_samples = [int(t * sample_rate) for t in cut_times]
            cut_samples.append(-1)
            cut_ranges = [(i, cut_samples[i], cut_samples[i+1]) for i in xrange(len(cut_samples) - 1)]
            for i, start, stop in tqdm(cut_ranges):
                if stop - start < sample_rate * 1.5:
                    continue
                output_file_path = "{}_{}.wav".format(
                    os.path.join(output_dir, output_filename_prefix),
                    convertTime(start, sample_rate)+'_'+convertTime(stop, sample_rate)
                )
                if dry_run:
                    print "Writing file {}".format(output_file_path)
                    wavfile.write(
                        filename=output_file_path,
                        rate=sample_rate,
                        data=samples[start:stop]
                    )
                else:
                    print "Not writing file {}".format(output_file_path)
