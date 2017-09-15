#!/bin/bash

. path_config.sh || exit 1;

model_dir=$1
no_utts=$2
type=$3
#type=live_questions
#src=/home/samf/NetBeansProjects/MillionQuiz/resource/jsgfs/$type
#src=/home/samf/quizdialogue/trunk/MillionQuiz/resource/jsgfs/$type
#src=generated_jsgfs/$type

#name=pioneer
#cd grammar/jsgf-dialogue
#
cd jsgf-dialogue

mkdir -p $type
mkdir -p $type/compiled


let range=no_utts-1
#
for i in `seq 0 $range`;
do 
	#cp $src/$i.jsgf $type || exit 1
    ./question_jsgf_to_fsm.sh $i $type || exit 1
    
    ./question_fsm_to_fst.sh $i $type  || exit 1
done

./question_n_grammar_lang.sh $type $no_utts || exit 1
##
for i in `seq 0 $range`;
do 
graph=$type/graph-$i  || exit 1
rm -rf $graph
./question_my-mkgraph.sh $i  $model_dir $graph  $type || exit 1
done

#done

#./jsgf_to_fsm.sh $name
#./fsm_to_fst.sh $name
#./make_grammar_lang.sh $name
#./my-mkgraph.sh $model_dir $graph



