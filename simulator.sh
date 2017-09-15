#!/bin/bash

#. config.sh

#interactive=false
read_pipe=$1
echo "read_pipe $read_pipe"


#graph=jsgf-dialogue/dialogue/graph-0

online_dir=online-models/nnet_noisy_online


start_listen=true
output_path=speech-out
record_wav=ON

keyphrase=HELLO_ZENO_I_AM_READY_TO_START

source=wav
decoder=nnet

date=`date +"%d_%m_%Y_%H_%M_%S"`
day=`date +"%d_%m_%Y"`

mkdir -p speech-out/$day/stdouts
mkdir -p speech-out/$day/speech
mkdir -p speech-out/$day/text-wav-eval
mkdir -p speech-out/$day/controls
mkdir -p speech-out/$day/chunks

args=( $online_dir $source $output_path $keyphrase $record_wav $read_pipe $start_listen);



if [ "$decoder" = "nnet" ]; then
	echo "Doing nnet";
	./nnet-decode-sim.sh ${args[@]}
elif [ "$decoder" = "gmm" ]; then
	echo "Doing gmm";
	./gmm-decode.sh ${args[@]}
else
	echo "Invalid decoder, must be gmm or nnet";
fi


