#!/bin/bash
# Input parameters
pyint=python3
toolpath=$(dirname "$0")/../panel_client.py
serialport=/dev/ttyACM0
# Red test loop
echo Test red channel
for i in {0..50..1}
do
    $pyint $toolpath -p $serialport set $i 0 0
done
for i in {50..0..-1}
do
    $pyint $toolpath -p $serialport set $i 0 0
done
# Green test loop
echo Test green channel
for i in {0..50..1}
do
    $pyint $toolpath -p $serialport set 0 $i 0
done
for i in {50..0..-1}
do
    $pyint $toolpath -p $serialport set 0 $i 0
done
# Blue test loop
echo Test blue channel
for i in {0..50..1}
do
    $pyint $toolpath -p $serialport set 0 0 $i
done
for i in {50..0..-1}
do
    $pyint $toolpath -p $serialport set 0 0 $i
done
# RGB test loop
echo Test all channels
for i in {0..50..1}
do
    $pyint $toolpath -p $serialport set $i $i $i
done
for i in {50..0..-1}
do
    $pyint $toolpath -p $serialport set $i $i $i
done
# EOF
