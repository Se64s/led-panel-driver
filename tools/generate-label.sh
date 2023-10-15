#!/bin/bash

# Help function ---------------------------------------------------------------

Help()
{
   # Display Help
   echo "Generate ppm image file with a text label."
   echo 
   echo "Syntax: $0 [w|H|T|t|c|o|h]"
   echo "options:"
   echo "w     Image width."
   echo "H     Image high."
   echo "T     Text high."
   echo "t     Text to print."
   echo "c     Color value in hex: 'RR/GG/BB'."
   echo "o     Output file name."
   echo "h     Show help."
   echo
}

# Main code -------------------------------------------------------------------

width=72
high=12
text_high=6
tmp_file_path=$(dirname "$0")/tmp_label.ppm
str_msg="Hello World"
out_img=label.ppm
color_background=black
color_val=01/01/01

# Process args ----------------------------------------------------------------

while getopts 'w:H:T:t:c:o:h' OPTION; do
    case "$OPTION" in
        w)
            width=$OPTARG
            ;;
        H)
            high=$OPTARG
            ;;
        T)
            text_high=$OPTARG
            ;;
        t)
            str_msg="$OPTARG"
            ;;
        c)
            color_val=$OPTARG
            ;;
        o)
            out_img=$OPTARG
            ;;
        h)
            Help
            exit 0
            ;;
        ?)
            echo "Error: Invalid option"
            exit 1
            ;;
    esac
done

# Logic -----------------------------------------------------------------------

# Create base image
ppmmake black $width $high > $tmp_file_path

# Add label
ppmlabel -x 1 -y $text_high -size $text_high -background $color_background -color rgb:$color_val -text "$str_msg" $tmp_file_path > $out_img

# Remove tmp files
rm $tmp_file_path

# EOF
