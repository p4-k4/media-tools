
import os
import ast
import ffmpeg
import subprocess
from subprocess import Popen, PIPE

file_input = '/media/paka/Paka/development/loudness/sample.wav'
file_output = '/media/paka/Paka/development/loudness/output.wav'

target_i = -10
target_tp = 2.0
target_lra = 15

class Analyze:
    def __init__(self, file_input):

        self.cmd_analyze = f"ffmpeg -i {file_input} -hide_banner -loglevel info -filter:a loudnorm=print_format=json -f null -"
        self.file_input = file_input
        self.analysis = Popen(self.cmd_analyze, shell=True, stdout=PIPE, stderr=PIPE)
        self.output, err = self.analysis.communicate()

        self.result = "{"+err.decode().split("{")[1]
        self.result_dictionary = ast.literal_eval(self.result)

        self.input_i = self.result_dictionary['input_i']
        self.input_tp = self.result_dictionary['input_tp']
        self.input_lra = self.result_dictionary['input_lra']
        self.input_thresh = self.result_dictionary['input_thresh']
        self.output_i = self.result_dictionary['output_i']
        self.output_tp = self.result_dictionary['output_tp']
        self.output_lra = self.result_dictionary['output_lra']
        self.output_thresh = self.result_dictionary['output_thresh']
        self.normalization_type = self.result_dictionary['normalization_type']
        self.target_offset = self.result_dictionary['target_offset']

    def all_results(self):

        print(self.file_input)
        try:
            for k, v in self.result_dictionary.items():
                print(k+': ', v)
        except Exception as e:
            print('Recieved an exception error: ', e)

file_input_analyze = Analyze(file_input)

def process(*args):

    file_input_analyze.all_results()

    try:
        print('')
        print(f'Processing {file_input}')
        print('')

        cmd_process = f"ffmpeg-normalize sample.wav -pr -f -nt ebu -t {target_i} -tp {target_tp} -lrt {target_lra} -ar 48 -o output.wav"

        process = Popen(cmd_process, shell=True, stdout=PIPE, stderr=PIPE)
        process.wait()

        file_output_analyze = Analyze(file_output)

        print('')
        print(f'Complete!')
        print('')

        file_output_analyze.all_results()
    except Exception as e:

        if os.path.exists(file_output) == False:
            print('There was a problem with exporting the output file: ', e)

        if os.path.exists(file_output) == True:
            print('The file exists, but there was an exception error: ', e)


process(file_output)
