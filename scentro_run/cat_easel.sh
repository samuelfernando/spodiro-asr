#!/bin/bash

. ./cmd.sh ## You'll want to change cmd.sh to something that will work on your system.

. ./path.sh           ## This relates to the queue.

root=/home/samuel/museum-data/kaldi_data


#mkdir $augmented
#utils/fix_data_dir.sh $speed_train
#./data_sort.sh $augmented
files=(text utt2spk segments wav.scp feats.scp cmvn.scp)
#

dest=1234

for file in ${files[@]}; do
	echo $file
#	cat $speed_train/$file $train/$file > $augmented/$file.unsorted || exit 1
	cat $root/1/$file $root/2/$file $root/3/$file $root/4/$file > $root/$dest/$file.unsorted || exit 1
done

./data_sort.sh $root/$dest

utils/utt2spk_to_spk2utt.pl $root/$dest/utt2spk > $root/$dest/spk2utt

utils/validate_data_dir.sh $root/$dest



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
