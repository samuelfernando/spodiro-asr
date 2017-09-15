#!/bin/bash

. ./cmd.sh ## You'll want to change cmd.sh to something that will work on your system.
           ## This relates to the queue.

export root=/home/samuel/wsj-pf-data
export data=$root/data
export train=$data/balanced
export wsj_test=$data/wsj/head_eval_test/5dB
export pf_test=$data/pf/head_test/clean
export lang=$root/lang/wsj-pfstar-with-eval
export exp=$root/exp_balanced

#steps/train_mono.sh --nj 12 --cmd "$train_cmd" \
#	$train $lang $exp/mono0a || exit 1;

#utils/mkgraph.sh --mono $lang \
#   $exp/mono0a $exp/mono0a/graph

#steps/decode.sh --nj 10 --cmd "$decode_cmd" $exp/mono0a/graph \
#   $test $exp/mono0a/decode
steps/online/nnet2/extract_ivectors_online.sh --cmd "$train_cmd" --nj 13 \
    ${wsj_test}_hires $exp/nnet2_online/extractor $exp/nnet2_online/ivectors_wsj_head_5dB


steps/online/nnet2/extract_ivectors_online.sh --cmd "$train_cmd" --nj 30 \
    ${pf_test}_hires $exp/nnet2_online/extractor $exp/nnet2_online/ivectors_pf_head_clean


#local/online/sam_run_nnet2_common.sh
#local/online/ivectors_test.sh
#local/online/ivectors_pf.sh

#utils/mkgraph.sh $lang $exp/tri4a $exp/tri4a/graph

#steps/decode_fmllr.sh --nj 13 --cmd "$decode_cmd" $exp/tri4a/graph \
#   $test $exp/tri4a/decode


#wsj1=/data/corpora0/LDC94S13B

#local/online/sam_run_nnet2_common.sh
