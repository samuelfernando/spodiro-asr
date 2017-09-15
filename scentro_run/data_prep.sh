#!/bin/bash

. ./cmd.sh ## You'll want to change cmd.sh to something that will work on your system.

. ./path.sh           ## This relates to the queue.

root=/home/samuel/wsj-pf-data
data=$root/data
speed_train=$data/pf/speed_train
train=$data/train-wsj-pf-inc-noise
augmented=$data/augmented-train-wsj-pf
augmented_easel=$data/augmented-train-wsj-pf-easel-0.8

#mkdir $augmented
#utils/fix_data_dir.sh $speed_train
data=/home/samf/Documents/art_data/lc_kaldi_art_8

#./data_sort.sh $data
#files=(text utt2spk segments wav.scp feats.scp cmvn.scp)
#
#for file in ${files[@]}; do
#	echo $file
#	cat $speed_train/$file $train/$file > $augmented/$file.unsorted || exit 1
#done

#utils/utt2spk_to_spk2utt.pl $data/utt2spk > $data/spk2utt

utils/validate_data_dir.sh $data


#steps/train_mono.sh --nj 12 --cmd "$train_cmd" \
#	$train $lang $exp/mono0a || exit 1;

#utils/mkgraph.sh --mono $lang \
#   $exp/mono0a $exp/mono0a/graph

#steps/decode.sh --nj 10 --cmd "$decode_cmd" $exp/mono0a/graph \
#   $test $exp/mono0a/decode
 
 
#local/online/ivectors_test.sh
#local/online/ivectors_pf.sh

#utils/mkgraph.sh $lang $exp/tri4a $exp/tri4a/graph

#steps/decode_fmllr.sh --nj 13 --cmd "$decode_cmd" $exp/tri4a/graph \
#   $test $exp/tri4a/decode
           
           
#wsj1=/data/corpora0/LDC94S13B

#local/online/sam_run_nnet2_common.sh
