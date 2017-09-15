#!/bin/bash

. ./cmd.sh ## You'll want to change cmd.sh to something that will work on your system.
           ## This relates to the queue.

root=/home/samuel/wsj-pf-data
data=$root/data
#train=$data/train-wsj-pf-inc-noise
#test=$data/wsj/head_eval_test/clean
train=$data/augmented-train-wsj-pf
lang=$root/lang/wsj-pfstar-with-eval

exp=$root/exp_augmented

#dir=$exp/nnet2_online/hidden5_nnet_ms_a_1epoch_learn1000
#dir=$exp/nnet2_online/hidden6_nnet_ms_a_1epoch
#srcdir=$exp/nnet2_online/nnet_a_gpu_baseline_0.25_epoch_online

#dir=exp/nnet2_online/nnet_a_gpu_baseline

#steps/online/nnet2/prepare_online_decoding.sh $lang "$dir" ${dir}_online || exit 1;

#dir=$exp/nnet2_online_wsj_pf/nnet_a_tri5a
#dir=$exp/nnet2_online/nnet_a_gpu_baseline_0.25_epoch_online
 #graph=/home/samuel/museum-data/healthy_graph 
#test=/home/samuel/museum-data/kaldi_data/0 
# graph=$exp/tri5a_museum/graph_wsj_pf_museum

dir=$exp/nnet2_online/nnet_ms_a
    
    # graph=$exp/tri4a/healthy_graph
#steps/online/nnet2/prepare_online_decoding.sh  --mfcc-config conf/mfcc_hires.conf \
#    $lang $exp/nnet2_online/extractor "$dir" ${dir}_online || exit 1;
 
graph=$exp/tri4a/graph
test=$data/pf/head_test/clean
 srcdir=$exp/nnet2_online/nnet_ms_a
   
 
 
 # for epoch in 1 2 3 4; do
 #   # do the actual online decoding with iVectors, carrying info forward from 
 #   # previous utterances of the same speaker.
 #   # We just do the bd_tgpr decodes; otherwise the number of combinations 
 #   # starts to get very large.
 #       steps/online/nnet2/decode.sh --cmd "$decode_cmd" --nj 8 --iter smbr_epoch${epoch} \
 #         $graph $test ${srcdir}_online/decode_smbr_epoch${epoch}
 # done
 
   # for epoch in 1 2 3 4; do
   # cp ${srcdir}_smbr/epoch${epoch}.mdl ${srcdir}_online/smbr_epoch${epoch}.mdl
  #done

  #time steps/online/nnet2/decode.sh  --cmd "$decode_cmd" --nj 20 \
   # $graph $test ${dir}_online/decode_museum_0_grammar 
#lang=/home/samuel/museum-data/wsj-pfstar-with-museum
 #   graph=$exp/tri4a/graph_wsj_pf_museum

#steps/online/nnet2/prepare_online_decoding_retrain.sh $srcdir "$dir" ${dir}_online || exit 1;

 #steps/online/nnet2/decode.sh  --cmd "$decode_cmd" --nj 32 \
 #   $graph $test ${dir}_online/decode_museum_0_wsj_pf_museum 

 # adapt=/home/samuel/museum-data/kaldi_data/1234
# lang=/home/samuel/museum-data/wsj-pfstar-with-eval
 graph=$exp/tri5a_museum/graph_wsj_pf_museum
test=/home/samuel/museum-data/kaldi_data/0
dir=$exp/tri5a_museum_online
#  steps/online/prepare_online_decoding.sh $train $lang $exp/tri5a_museum $exp/tri5a_museum_online
 steps/online/prepare_online_decoding.sh $train $lang $exp/tri3b $exp/tri3b_online 
#  time steps/decode_fmllr.sh --nj 32 --cmd "$decode_cmd" $graph \
 #  $test $exp/tri4a/decode_museum_0_wsj_pf_museum
#utils/validate_data_dir.sh $test
 #steps/online/decode.sh --cmd "$decode_cmd"  --nj 30 $graph $test $dir/decode_museum_0_wsj_pf_museum
 #steps/decode_fmllr.sh --nj 30 $graph $test $exp/tri5a_museum_online/decode_museum_0_wsj_pf_museum
 
# steps/online/decode.sh $graph $test $exp/tri4a_online/decode_museum_0_wsj_pf_museum
 #adapt=/home/samuel/museum-data/kaldi_data/1234
 
# steps/align_fmllr.sh --nj 32 --cmd "$train_cmd" $adapt $lang $exp/tri4a $exp/tri4a_ali_museum || exit 1;

 #steps/train_sat.sh  --cmd "$train_cmd" 4200 40000 $adapt $lang $exp/tri4a_ali_museum $exp/tri5a_museum || exit 1;

# graph=$exp/tri5a_museum/graph_wsj_pf_museum
 #utils/mkgraph.sh $lang $exp/tri5a_museum $graph
 
 #steps/decode_fmllr.sh --nj 32 --cmd "$decode_cmd" $graph \
 #  $test $exp/tri5a_museum/decode_museum_0_wsj_pf_museum
