#!/bin/bash

. ./cmd.sh ## You'll want to change cmd.sh to something that will work on your system.
           ## This relates to the queue.

root=/home/samuel/wsj-pf-data
data=$root/data
#train=$data/train-wsj-pf-inc-noise
#test=$data/wsj/head_eval_test/clean
lang=$root/lang/wsj-pfstar-with-eval
exp=$root/exp_augmented
#dir=$exp/nnet2_online/hidden5_nnet_ms_a_1epoch_learn1000
#dir=$exp/nnet2_online/hidden6_nnet_ms_a_1epoch
dir=$exp/nnet2_online/nnet_ms_a
#steps/train_mono.sh --nj 12 --cmd "$train_cmd" \
#	$train $lang $exp/mono0a || exit 1;

#utils/mkgraph.sh --mono $lang \
#   $exp/mono0a $exp/mono0a/graph

#steps/decode.sh --nj 10 --cmd "$decode_cmd" $exp/mono0a/graph \
#   $test $exp/mono0a/decode
 
#local/online/sam_run_nnet2.sh   
#local/online/ivectors_test.sh
#utils/mkgraph.sh $lang $exp/tri4a $exp/tri4a/graph

#steps/decode_fmllr.sh --nj 13 --cmd "$decode_cmd" $exp/tri4a/graph \
#   $test $exp/tri4a/decode

datadir=head_eval_test
subdir=5dB

steps/online/nnet2/extract_ivectors_online.sh --cmd "$train_cmd" --nj 13 \
      $data/wsj/$datadir/${subdir}_hires $exp/nnet2_online/extractor $exp/nnet2_online/ivectors_wsj_${datadir}_${subdir} || exit 1 
 
datadir=head_test
subdir=clean

steps/online/nnet2/extract_ivectors_online.sh --cmd "$train_cmd" --nj 40 \
      $data/pf/$datadir/${subdir}_hires $exp/nnet2_online/extractor $exp/nnet2_online/ivectors_pf_${datadir}_${subdir} || exit 1

     steps/nnet2/decode.sh --nj 13 --cmd "$decode_cmd" \
          --online-ivector-dir $exp/nnet2_online/ivectors_wsj_head_eval_test_5dB \
         $exp/tri4a/graph $data/wsj/head_eval_test/5dB_hires $dir/decode_head_5dB || exit 1;
              steps/nnet2/decode.sh --nj 60 --cmd "$decode_cmd" \
          --online-ivector-dir $exp/nnet2_online/ivectors_pf_head_test_clean \
         $exp/tri4a/graph $data/pf/head_test/clean_hires $dir/decode_pf_head_clean || exit 1;

#wsj1=/data/corpora0/LDC94S13B

#local/online/sam_run_nnet2_common.sh
