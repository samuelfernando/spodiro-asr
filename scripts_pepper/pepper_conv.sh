#!/bin/bash

echo $1
infile=$1

sox -c 1 -e signed -r 16000 -b 16 ${infile}_0.raw ${infile}_0.wav
sox -c 1 -e signed -r 16000 -b 16 ${infile}_1.raw ${infile}_1.wav
sox -c 1 -e signed -r 16000 -b 16 ${infile}_2.raw ${infile}_2.wav
sox -c 1 -e signed -r 16000 -b 16 ${infile}_3.raw ${infile}_3.wav

