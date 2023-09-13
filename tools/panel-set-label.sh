#!/bin/bash

# Help function ---------------------------------------------------------------
Help()
{
   # Display Help
   echo "Send text label to panel server."
   echo 
   echo "Syntax: $0 [p|t|c|h]"
   echo "Options:"
   echo "p     Serial port."
   echo "t     Text to show."
   echo "c     Text color, color value in hex: 'RR/GG/BB'."
   echo "h     Show help."
   echo
}

# Main code -------------------------------------------------------------------

# Input parameters
pyint=python3
tmp_file_path=$(dirname "$0")/tmp_tool.ppm
panel_server_path=$(dirname "$0")/../panel_client.py
label_gen_path=$(dirname "$0")/generate-label.sh
label_text="Hello World"
label_color=10/10/10
port=/dev/ttyACM0

# Process args ----------------------------------------------------------------

while getopts 'p:t:c:h' OPTION; do
    case "$OPTION" in
        p)
            port=$OPTARG
            ;;
        t)
            label_text="$OPTARG"
            ;;
        c)
            label_color=$OPTARG
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

# Generate label
$label_gen_path -t "$label_text" -c $label_color -o $tmp_file_path

# Send label to server
$pyint $panel_server_path -p $port image $tmp_file_path

# Clear temp file
rm $tmp_file_path

# EOF
