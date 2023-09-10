#!/bin/bash
# Input parameters
pyint=python3
tmp_file_path=$(dirname "$0")/tmp_tool.ppm
toolpath=$(dirname "$0")/../panel_client.py
label_gen_path=$(dirname "$0")/generate-label.sh
serialport=/dev/ttyACM0
# Generate label
$label_gen_path "$1" $tmp_file_path
# Send label to server
$pyint $toolpath -p $serialport image $tmp_file_path
rm $tmp_file_path
# EOF
