#!/bin/bash
# Input parameters
pyint=python3
tmp_file_path=$(dirname "$0")/tmp_tool.ppm
toolpath=$(dirname "$0")/../panel_client.py
label_gen_path=$(dirname "$0")/generate-label.sh
serialport=/dev/ttyACM0
message_list=(
    'Hola_Mundo'
    'MUY BUENOS DIAS'
    'CARMEN_<3'
)
# Loop for each image
for val1 in ${message_list[*]}; do
    $label_gen_path -t "$val1" -o $tmp_file_path
    $pyint $toolpath -p $serialport image $tmp_file_path
    sleep 1
    rm $tmp_file_path
    $pyint $toolpath -p $serialport clear
done
# EOF
