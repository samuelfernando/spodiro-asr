#!/bin/bash

# this is our online-nnet2 build.  it's a "multi-splice" system (i.e. we have
# splicing at various layers), with p-norm nonlinearities.  We use the "accel2"
# script which uses between 2 and 14 GPUs depending how far through training it
# is.  You can safely reduce the --num-jobs-final to however many GPUs you have
# on your system.

# For joint training with RM, this script is run using the following command line,
# and note that the --stage 8 option is only needed in case you already ran the
# earlier stages.
# local/online/run_nnet2.sh --stage 8 --dir exp/nnet2_online/nnet_ms_a_partial --exit-train-stage 15

. cmd.sh


stage=0
train_stage=-10
use_gpu=true
dir=$exp/nnet2_online/hidden5_nnet_ms_a
exit_train_stage=-100
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
  parallel_opts="--gpu 1" 
  num_threads=1
  minibatch_size=512
  # the _a is in case I want to change the parameters.
else
  num_threads=16
  minibatch_size=128
  parallel_opts="--num-threads $num_threads" 
fi

#local/online/sam_run_nnet2_common.sh --stage $stage || exit 1;

#echo ${train}_hires, $lang, $exp, $dir
#exit 0

if [ $stage -le 8 ]; then
  # last splicing was instead: layer3/-4:2" 
for hid_lay in `seq 1 6`;
do
	for lr in 001 002 005 01 ;
	do
		init_lr=0.$lr
		final_lr=0.0$lr
		for pnorm in 100 200 300 ;
		do
			
input_p=${pnorm}0
output_p=$pnorm
echo $hid_lay $init_lr $final_lr $input_p $output_p
dir_name=nnet-$hid_lay-$init_lr-$final_lr-$input_p-$output_p

echo $dir_name

steps/nnet2/train_multisplice_accel2.sh --stage $train_stage \
    --exit-stage $exit_train_stage \
    --num-epochs 1 --num-jobs-initial 2 --num-jobs-final 8 \
    --num-hidden-layers $hid_lay \
    --splice-indexes "layer0/-1:0:1 layer1/-2:1 layer2/-4:2" \
    --feat-type raw \
    --online-ivector-dir $exp/nnet2_online/ivectors_train \
    --cmvn-opts "--norm-means=false --norm-vars=false" \
    --num-threads "$num_threads" \
    --minibatch-size "$minibatch_size" \
    --parallel-opts "$parallel_opts" \
    --io-opts "--max-jobs-run 12" \
    --initial-effective-lrate $init_lr --final-effective-lrate $final_lr \
    --cmd "$decode_cmd" \
    --pnorm-input-dim $input_p \
    --pnorm-output-dim $output_p \
    --mix-up 12000 \
    ${train}_hires $lang $exp/nnet2_online/tri4a_ali $exp/nnet2_online/$dir_name  || exit 1;
    
done
done
done

fi

exit 0

