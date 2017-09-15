#!/bin/bash

#. config.sh

#interactive=false
read_pipe=999
#echo "read_pipe $read_pipe"

#graph=models/healthy_graph
#graph=models/fisher_graph
#graph=models/graph-spodiro_complete-gmm
#graph=models/graph-healthy_living_complete-gmm
#graph=models/graph-number_game-gmm
#graph=/home/samf/spodiro-asr/models/spodiro_graph
#graph=models/graph-wsj-pfstar-with-museum-gmm
#graph=models/graph_wsj_pf_museum
#graph=/home/samf/spodiro-asr/models/wsj_pepper_graph

graph=/home/samf/spodiro-asr/models/pepper-grammar-graph

#graph=jsgf-dialogue/dialogue/graph-0
#online_dir=/home/samf/spodiro-asr/online-models/nnet_noisy_online
online_dir=/home/samf/spodiro-asr/online-models/pepper_nnet_online
#online_dir=models/nnet_a_online
#online_dir=online-models/fisher_nnet_online
#

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
	/home/samf/spodiro-asr/nnet-decode-pepper.sh ${args[@]}
elif [ "$decoder" = "gmm" ]; then
	echo "Doing gmm";
	./gmm-decode.sh ${args[@]}
else
	echo "Invalid decoder, must be gmm or nnet";
fi


