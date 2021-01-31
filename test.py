#!/usr/bin/env python3
import os
import ast
import sys
import subprocess
from subprocess import Popen, PIPE


file_input = '/media/paka/Paka/development/loudness/sample.wav'
file_output = '/media/paka/Paka/development/loudness/output.wav'

def analyze(file_input):
    cmd_analyze = f"ffmpeg -i {file_input} -hide_banner -loglevel info -filter:a loudnorm=print_format=json -f null -"

    try:
        output = subprocess.Popen(cmd_analyze, shell=True, stdout=PIPE, stderr=PIPE)
        output, err = output.communicate()
        formatted_string = "{"+err.decode().split("{")[1]
        string_to_dict = ast.literal_eval(formatted_string)
        return(string_to_dict)


    except Exception as e:
        return 'Recieved exception error!'

def process(file_input, file_output):
    cmd_process = f"ffmpeg -i {file_input} \
                    -af loudnorm=I={target_i}:\
                    TP={target_tp}:LRA={target_lra}:\
                    measured_I={check.measured_input_i}:\
                    measured_LRA={check.measured_input_lra}:\
                    measured_TP={check.measured_input_tp}:\
                    measured_thresh={check.measured_input_thresh}:\
                    offset={check.measured_target_offset}:\
                    linear=true:print_format=summary -ar 48k output.wav -y"

    output = Popen(cmd_process, stdout=PIPE)

    try:
        output = subprocess.Popen(cmd_analyze, shell=True, stdout=PIPE, stderr=PIPE)
        output, err = output.communicate()
        formatted_string = "{"+err.decode().split("{")[1]
        string_to_dict = ast.literal_eval(formatted_string)
        print(string_to_dict)

    except Exception as e:
        return 'Recieved exception error!'




analyze(file_input)
#process(file_input, file_output)
