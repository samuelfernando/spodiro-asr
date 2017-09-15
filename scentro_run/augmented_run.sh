#!/bin/bash

. ./cmd.sh ## You'll want to change cmd.sh to something that will work on your system.
           ## This relates to the queue.

export root=/home/samuel/wsj-pf-data
export data=$root/data
#export train=$data/augmented-train-wsj-pf
export train=$data/augmented-train-wsj-pf
export test=$data/wsj/head_eval_test/clean
export lang=$root/lang/wsj-pfstar-with-eval
export exp=$root/exp_augmented
export adapt=/home/samuel/museum-data/kaldi_data/1234

#steps/train_mono.sh --nj 12 --cmd "$train_cmd" \
#	$train $lang $exp/mono0a || exit 1;

#utils/mkgraph.sh --mono $lang \
#   $exp/mono0a $exp/mono0a/graph

#steps/decode.sh --nj 10 --cmd "$decode_cmd" $exp/mono0a/graph \
#   $test $exp/mono0a/decode
 
#local/online/sam_run_nnet2_baseline.sh   

local/online/sam_run_nnet2_discriminative.sh
#./retrain.sh
#local/online/ivectors_test.sh
#local/online/ivectors_pf.sh

#utils/mkgraph.sh $lang $exp/tri4a $exp/tri4a/graph

#steps/decode_fmllr.sh --nj 13 --cmd "$decode_cmd" $exp/tri4a/graph \
#   $test $exp/tri4a/decode
           
           
#wsj1=/data/corpora0/LDC94S13B

#local/online/sam_run_nnet2_common.sh
