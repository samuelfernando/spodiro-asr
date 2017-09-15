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

keyphrase=HELLO_ZENO_ARE_YOU_READY_TO_START

source=pa
decoder=nnet


args=( $online_dir $source $output_path $keyphrase $record_wav $read_pipe $start_listen);


if [ ! -d "speech-out" ]; then
	mkdir speech-out
	mkdir speech-out/text
	mkdir speech-out/chunks
	mkdir speech-out/text-wav-eval
	mkdir speech-out/speech
	mkdir speech-out/stdouts	
	mkdir speech-out/controls
fi

if [ "$decoder" = "nnet" ]; then
	echo "Doing nnet";
	./nnet-decode.sh ${args[@]}
elif [ "$decoder" = "gmm" ]; then
	echo "Doing gmm";
	./gmm-decode.sh ${args[@]}
else
	echo "Invalid decoder, must be gmm or nnet";
fi


