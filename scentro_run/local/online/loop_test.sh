#!/bin/bash

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
			echo nnet-$hid_lay-$init_lr-$final_lr-$input_p-$output_p
		done
	done				
done