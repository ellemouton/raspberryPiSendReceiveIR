#!/bin/bash
echo Modulating and checking text file.....
sudo pigpiod

python modulate.py &
python sendFromText.py
wait
