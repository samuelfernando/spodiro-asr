#!/bin/bash

. ./cmd.sh ## You'll want to change cmd.sh to something that will work on your system.
           ## This relates to the queue.

root=/home/samuel/wsj-pf-data
data=$root/data
train=$data/train-wsj-pf-inc-noise
#test=$data/wsj/head_eval_test/clean
test=$data/pf/head_test/clean
lang=$root/lang/wsj-pfstar-with-eval
#exp=$root/exp_augmented
exp=$root/exp
#dir=$exp/nnet2_online/hidden5_nnet_ms_a_1epoch_learn1000
#dir=$exp/nnet2_online/hidden6_nnet_ms_a_1epoch
#dir=$exp/nnet2_online/large_learning_mdl
#steps/train_mono.sh --nj 12 --cmd "$train_cmd" \
dir=$exp/tri4a
#	$train $lang $exp/mono0a || exit 1;

#utils/mkgraph.sh --mono $lang \
#   $exp/mono0a $exp/mono0a/graph

#steps/decode.sh --nj 10 --cmd "$decode_cmd" $exp/mono0a/graph \
#   $test $exp/mono0a/decode
 
#local/online/sam_run_nnet2.sh   
#local/online/ivectors_test.sh
#utils/mkgraph.sh $lang $exp/tri4a $exp/tri4a/graph

#steps/decode_fmllr.sh --nj 32 --cmd "$decode_cmd" $exp/tri4a/graph \
#   $test $exp/tri4a/decode_pf_clean
#local/online/sam_run_nnet2_common.sh
#dir=$exp/nnet2_online_wsj_pf/nnet_a
 graph=/home/samuel/museum-data/healthy_graph 
test=/home/samuel/museum-data/kaldi_data/0 

steps/decode_fmllr.sh --nj 32 --cmd "$decode_cmd" $dir/graph_healthy \
   $test $dir/decode_museum_0_grammar
