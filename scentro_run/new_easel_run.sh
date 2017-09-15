#!/bin/bash

. ./cmd.sh ## You'll want to change cmd.sh to something that will work on your system.
           ## This relates to the queue.
#export train=$data/augmented-train-wsj-pf
#export train=$data/augmented-train-wsj-pf-easel0.8
root_data=/home/samuel/museum-data
root_model=/home/samuel/wsj-pf-data
test=$root_data/kaldi_data/0
lang=$root_data/wsj-pfstar-with-museum
exp=$root_model/exp_augmented


#graph_name=healthy_graph
#graph_name=fisher_bigram_filtered_graph
graph_name=fisher_bigram_zeeno_graph
#graph=$exp/tri4a/graph_wsj_pf_museum
graph=$exp/tri4a/${graph_name}
#graph=$exp/tri4a/spodiro_graph
dir=$exp/nnet2_online_wsj_pf/nnet_a_online
#export adapt=/home/samuel/museum-data/kaldi_data/1234
echo $graph
#steps/train_mono.sh --nj 12 --cmd "$train_cmd" \
#	$train $lang $exp/mono0a || exit 1;

#utils/mkgraph.sh --mono $lang \
#   $exp/mono0a $exp/mono0a/graph

#steps/decode.sh --nj 10 --cmd "$decode_cmd" $exp/mono0a/graph \
#   $test $exp/mono0a/decode
 
local/online/sam_run_nnet2_baseline.sh   

#steps/online/nnet2/decode.sh --threaded true --do-endpointing true --nj 1 $graph $test $dir/decode_museum_0_wsj_pf_threaded_1_2_end
#decode=$dir/decode_${graph_name}_threaded_4_4_new_end
#decode=$dir/decode_${graph_name}_threaded_4_4
#rm -rf $decode
#steps/online/nnet2/decode.sh --threaded true --do-endpointing true --nj 4 $graph $test $decode
#./retrain.sh
#local/online/ivectors_test.sh
#local/online/ivectors_pf.sh

#utils/mkgraph.sh $lang $exp/tri4a $exp/tri4a/graph

#steps/decode_fmllr.sh --nj 13 --cmd "$decode_cmd" $exp/tri4a/graph \
#   $test $exp/tri4a/decode
           
           
#wsj1=/data/corpora0/LDC94S13B

#local/online/sam_run_nnet2_common.sh
