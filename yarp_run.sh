#!/bin/bash

#./quad_ros_input samf-scripts/quad_online.sh
my_date=`date +"%Y-%m-%d-%T"`
full_path=speech-out/stdouts/$my_date.txt
port_name="/SpeechRecognition/Sentence:o"

yarp-out/easel ./new_recogniser.sh "$port_name" 2>&1 | tee $full_path

#yarp-out/act_input ./laptop_online.sh 2>&1 | tee $full_path
