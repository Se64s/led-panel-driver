#!/bin/bash
# Get tool parameters
pyint=$1
pytoolpath=$2
pyport=$3
pybaudrate=$4
# Define project folders
pfolders=(
    "lib"
)
# Define project sources
psources=(
    "lib/led_panel_handler.py"
    "lib/link_layer.py"
    "lib/cmd_layer.py"
    "main.py"
)
# Create folders
echo " - Setup project folders:"
for val1 in ${pfolders[*]}; do
    $pyint $pytoolpath "-d" $pyport "-b" $pybaudrate "-f" "mkdir" $val1
done
# Create sources
echo " - Copy sources into device:"
for val1 in ${psources[*]}; do
    $pyint $pytoolpath "-d" $pyport "-b" $pybaudrate "-f" "cp" $val1 :$val1
done

# EOF
