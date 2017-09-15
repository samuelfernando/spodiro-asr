#!/bin/bash

#. path_config.sh || exit 1;

model_dir=../online-models/offline-tri4a-acoustic

type=$1
no_utts=$2

#type=live_questions
#src=/home/samf/NetBeansProjects/MillionQuiz/resource/jsgfs/$type
#src=/home/samf/quizdialogue/trunk/MillionQuiz/resource/jsgfs/$type

jsgf-dialogue/sub_grammar.sh $model_dir $no_utts $type || exit 1;




