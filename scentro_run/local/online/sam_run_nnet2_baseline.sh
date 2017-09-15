#!/bin/bash

. cmd.sh


stage=1
train_stage=0
use_gpu=true
. cmd.sh
. ./path.sh
. ./utils/parse_options.sh

exp=/scratch/samuel/exp_perturb
train=/home/samuel/wsj-pf-data/data/wsj/train-all-perturb
lang=/home/samf/wsj-p-data/lang/wsj_fisher_lang_test

lang=
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
  # the _a is in case I want to change the parameters.
  dir=$exp/nnet2_online/nnet_a_gpu_baseline_0.25_epoch
else
  # Use 4 nnet jobs just like run_4d_gpu.sh so the results should be
  # almost the same, but this may be a little bit slow.
  num_threads=16
  minibatch_size=128
  parallel_opts="-pe smp $num_threads" 
  dir=$exp/nnet2_online/nnet_a_baseline
fi




  # train without iVectors.
  steps/nnet2/train_pnorm_fast.sh --stage $train_stage \
    --num-epochs 2 --num-epochs-extra 1 \
    --splice-width 7 --feat-type raw \
    --cmvn-opts "--norm-means=false --norm-vars=false" \
    --num-threads "$num_threads" \
    --minibatch-size "$minibatch_size" \
    --parallel-opts "$parallel_opts" \
    --num-jobs-nnet 6 \
    --num-hidden-layers 4 \
    --mix-up 4000 \
    --initial-learning-rate 0.02 --final-learning-rate 0.004 \
    --cmd "$decode_cmd" \
    --pnorm-input-dim 2400 \
    --pnorm-output-dim 300 \
    $train $lang $exp/nnet2_online/tri4a_ali $dir  || exit 1;



 steps/nnet2/decode.sh --nj 13 --cmd "$decode_cmd" \
         $exp/tri4a/graph $test $dir/decode || exit 1;

