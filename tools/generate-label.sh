#!/bin/bash
width=72
high=6
text_high=5
tmp_file_path=$(dirname "$0")/tmp_label.ppm
# str_msg="HOLA MUNDO"
str_msg="$1"
# out_img=test_msg.ppm
out_img=$2
color_background=black
color_text=rgb:15/00/15
# Create base image
ppmmake black $width $high > $tmp_file_path
ppmlabel -x 2 -y $text_high -size $text_high -background $color_background -color $color_text -text "$str_msg" $tmp_file_path > $out_img
rm $tmp_file_path
# EOF
