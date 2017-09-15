#!/bin/bash

# this script is called from scripts like run_nnet2.sh; it does
# the common stages of the build.


. cmd.sh
. ./path.sh
. ./utils/parse_options.sh

njobs=13
#. cmd.sh
#. ./path.sh

#echo $data, $exp

rm $exp/nnet2_online/.error 2>/dev/null
# 
for datadir in head_eval_test; do
##	for subdir in clean 5dB 10dB 20dB; do
  #for datadir in $train; do
  for subdir in 5dB; do
    steps/online/nnet2/extract_ivectors_online.sh --cmd "$train_cmd" --nj $njobs \
      $data/wsj/$datadir/${subdir}_hires $exp/nnet2_online/extractor $exp/nnet2_online/ivectors_wsj_${datadir}_${subdir} || touch $exp/nnet2_online/.error &
  done
done
wait
[ -f $exp/nnet2_online/.error ] && echo "$0: error extracting iVectors." && exit 1;
#
exit 0;
#
