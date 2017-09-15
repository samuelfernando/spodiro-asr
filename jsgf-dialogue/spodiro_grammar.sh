#!/bin/bash

. path.sh || exit 1;

#name=fisher_06062016
#name=healthy_living_complete
name=spodiro_complete

#name=wsj-pfstar-with-museum
#model_dir=../online-models/offline-tri4a-acoustic

#model_dir=../online-models/offline_wsj_pfstar_tri4b
#model_dir=../online-models/tri4a-nnet-acoustic
#graph=../online-models/graph-$name-nnet
#graph=../online-models/graph-$name-gmm


#name=pioneer
#cd grammar

./jsgf_to_fsm.sh $name
#./fsm_to_fst.sh $name
#./make_grammar_lang.sh $name

#./my-mkgraph.sh $model_dir $graph
#./make_fisher_lang.sh 

#rm -rf $graph

#utils/mkgraph.sh $name $model_dir $graph

