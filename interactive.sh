#!/bin/bash

. config.sh

read_pipe=$0
echo "Read pipe $read_pipe"
#graph=online-models/graph-questions-worksheet-grammar
graph=online-models/wsj_pf_question_grammar

#graph=online-models/graph-smalltalk

#online_dir=online-models/tri4b_farfield_online
online_dir=online-models/wsj_pfstar_tri4b_online
start_listen=true
output_path=speech-out
record_wav=OFF
keyphrase=HELLO_ZENO_ARE_YOU_READY_TO_START
source=pa

./interactive-decode.sh $graph $online_dir $source $output_path $keyphrase $record_wav $read_pipe $start_listen


