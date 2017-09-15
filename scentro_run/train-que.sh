#!/bin/bash

# This is the training portion of the WSJ recipe (need to run mfcc.sh first)

#wsj1=/data/corpora0/LDC94S13B

. ./cmd.sh ## You'll want to change cmd.sh to something that will work on your system.
 
#. config.sh || exit 1


root=/home/samuel/wsj-pf-data
data=$root/data
train=$data/wsj/train-all-perturb
test=$data/wsj/lower-head_eval_test/clean
#lang=$root/lang/wsj-fisher-lang
lang=$root/lang/wsj_fisher_lang_test

exp=/scratch/samuel/exp_perturb

njobs=10
decode_jobs=13

#utils/subset_data_dir.sh --speakers $train 30000 ${train}_30k
#utils/subset_data_dir.sh --speakers $train 10000 ${train}_10k

steps/train_mono.sh --nj 4 --cmd "$train_cmd" ${train}_10k $lang $exp/mono0a || exit 1;

utils/mkgraph.sh --mono $lang $exp/mono0a $exp/mono0a/graph

steps/decode.sh --nj $decode_jobs --cmd "$decode_cmd" $exp/mono0a/graph $test $exp/mono0a/decode

steps/align_si.sh --nj $njobs --cmd "$train_cmd" ${train}_30k $lang $exp/mono0a $exp/mono0a_ali || exit 1;

steps/train_deltas.sh --cmd "$train_cmd" 2000 10000 ${train}_30k $lang $exp/mono0a_ali $exp/tri1 || exit 1;
    
utils/mkgraph.sh $lang $exp/tri1 $exp/tri1/graph || exit 1;
    
steps/decode.sh --nj $decode_jobs --cmd "$decode_cmd" $exp/tri1/graph $test $exp/tri1/decode 
     
steps/align_si.sh --nj $njobs --cmd "$train_cmd" ${train}_30k $lang $exp/tri1 $exp/tri1_ali || exit 1;

# Train tri2a, which is deltas + delta-deltas, on si84 $data.

steps/train_deltas.sh --cmd "$train_cmd" 2500 15000 ${train}_30k $lang $exp/tri1_ali $exp/tri2a || exit 1;

utils/mkgraph.sh $lang $exp/tri2a $exp/tri2a/graph || exit 1;

steps/decode.sh --nj $decode_jobs --cmd "$decode_cmd" $exp/tri2a/graph $test $exp/tri2a/decode || exit 1;

steps/align_si.sh --nj $njobs --cmd "$train_cmd" ${train}_30k $lang $exp/tri2a $exp/tri2a_ali || exit 1;

steps/train_lda_mllt.sh --cmd "$train_cmd" --splice-opts "--left-context=3 --right-context=3" 2500 15000 ${train}_30k $lang $exp/tri2a_ali $exp/tri2b || exit 1;

utils/mkgraph.sh $lang $exp/tri2b $exp/tri2b/graph || exit 1;

steps/decode.sh --nj $decode_jobs --cmd "$decode_cmd" $exp/tri2b/graph $test $exp/tri2b/decode || exit 1;


steps/align_si.sh  --nj $njobs --cmd "$train_cmd" --use-graphs true ${train}_30k $lang $exp/tri2b $exp/tri2b_ali  || exit 1;


steps/train_sat.sh --cmd "$train_cmd" 2500 15000 ${train}_30k $lang $exp/tri2b_ali $exp/tri3b || exit 1;

utils/mkgraph.sh $lang $exp/tri3b $exp/tri3b/graph || exit 1;

steps/decode_fmllr.sh --nj $decode_jobs --cmd "$decode_cmd" $exp/tri3b/graph $test $exp/tri3b/decode || exit 1;



steps/align_fmllr.sh --nj 12 --cmd "$train_cmd" $train $lang $exp/tri3b $exp/tri3b_ali || exit 1;


# From 3b system, train another SAT system (tri4a) with all the si284 $data.

steps/train_sat.sh  --cmd "$train_cmd" 4200 40000 $train $lang $exp/tri3b_ali $exp/tri4a || exit 1;

utils/mkgraph.sh $lang $exp/tri4a $exp/tri4a/graph || exit 1;

steps/decode_fmllr.sh --nj $decode_jobs --cmd "$decode_cmd" $exp/tri4a/graph $test $exp/tri4a/decode || exit 1;
 


