#!/bin/bash

#. config.sh

#interactive=false
read_pipe=$1
#echo "read_pipe $read_pipe"

graph=/home/samf/spodiro-asr/models/miro_grammar_graph
#graph=/home/samf/spodiro-asr/models/sil_miro_grammar


online_dir=/home/samf/spodiro-asr/online-models/miro_gpu_fast_online
#online_dir=/home/samf/spodiro-asr/online-models/sil_nnet_online


start_listen=true
output_path=speech-out
record_wav=ON

keyphrase=hello_i_am_ready

source=pa
decoder=nnet


args=( $graph $online_dir $source $output_path $keyphrase $record_wav $read_pipe $start_listen);

date=`date +"%d_%m_%Y_%H_%M_%S"`
day=`date +"%d_%m_%Y"`

mkdir -p speech-out/$day/stdouts
mkdir -p speech-out/$day/speech
mkdir -p speech-out/$day/text
mkdir -p speech-out/$day/controls
mkdir -p speech-out/$day/chunks

full_path=speech-out/$day/stdouts/$date.txt

if [ "$decoder" = "nnet" ]; then
	#echo "Doing nnet";
	/home/samf/spodiro-asr/nnet-decode-miro.sh ${args[@]}
elif [ "$decoder" = "gmm" ]; then
	#echo "Doing gmm";
	./gmm-decode.sh ${args[@]}
else
	echo "Invalid decoder, must be gmm or nnet";
fi


