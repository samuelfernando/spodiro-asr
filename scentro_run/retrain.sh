#!/bin/bash

# note: see the newer, better script run_nnet2_wsj_joint.sh

# This script assumes you have previously run the WSJ example script including
# the optional part local/online/run_online_decoding_nnet2.sh.  It builds a
# neural net for online decoding on top of the network we previously trained on
# WSJ, by keeping everything but the last layer of that network and then
# training just the last layer on our data.  We then train the whole thing.

stage=1
set -e

train_stage=-10
use_gpu=true
. cmd.sh
. ./path.sh
. ./utils/parse_options.sh

if $use_gpu; then
  if ! cuda-compiled; then
    cat <<EOF && exit 1 
This script is intended to be used with GPUs but you have not compiled Kaldi with CUDA 
If you want to use GPUs (and have them), go to src/, and configure and make on a machine
where "nvcc" is installed.  Otherwise, call this script with --use-gpu false
EOF
  fi
  parallel_opts="-l gpu=1" 
  num_threads=1
  minibatch_size=512
  dir=$exp/nnet2_online_wsj_pf/nnet_a_tri5a
  trainfeats=$exp/nnet2_online_wsj_pf/wsj_activations_train
  # later we'll change the script to download the trained model from kaldi-asr.org.
  srcdir=$exp/nnet2_online/nnet_a_gpu_baseline_0.25_epoch_online
else
  # Use 4 nnet jobs just like run_4d_gpu.sh so the results should be
  # almost the same, but this may be a little bit slow.
 echo "No GPU!"
	exit 1;
fi


if [ $stage -le 0 ]; then
  echo "$0: dumping activations from WSJ model"
  steps/online/nnet2/dump_nnet_activations.sh --cmd "$train_cmd" --nj 30 \
     $adapt $srcdir $trainfeats
fi


if [ $stage -le 1 ]; then
  echo "$0: training 0-hidden-layer model on top of WSJ activations"
 
  lang=/home/samuel/museum-data/wsj-pfstar-with-museum
  
steps/align_fmllr.sh --nj 40 --cmd "$train_cmd" \
    $adapt $lang $exp/tri5a_museum $exp/nnet2_online/tri5a_museum_ali

  steps/nnet2/retrain_fast.sh --stage $train_stage \
    --num-threads "$num_threads" \
    --minibatch-size "$minibatch_size" \
    --parallel-opts "$parallel_opts" \
    --cmd "$decode_cmd" \
    --num-jobs-nnet 4 \
    --mix-up 4000 \
    --initial-learning-rate 0.02 --final-learning-rate 0.004 \
     $trainfeats/data $lang $exp/nnet2_online/tri5a_museum_ali $dir 
fi

