#!/bin/bash

#./quad_ros_input samf-scripts/quad_online.sh
#my_date=`date +"%Y-%m-%d-%T"`
date=`date +"%d_%m_%Y_%H_%M_%S"`
day=`date +"%d_%m_%Y"`

mkdir -p speech-out/$day/stdouts
mkdir -p speech-out/$day/speech
mkdir -p speech-out/$day/text
mkdir -p speech-out/$day/controls
mkdir -p speech-out/$day/chunks

full_path=speech-out/$day/stdouts/$date.txt
port_name="/SpeechRecognition/Sentence:o"

#yarp-out/easel ./recogniser.sh "$port_name" 2>&1 | tee $full_path

#yarp-out/act_input ./laptop_online.sh 2>&1 | tee $full_path

yarp-out/new_asr_master "$port_name" 2>&1 | tee $full_path
