. ./cmd.sh
# Now make MFCC features.
# mfccdir should be some place with a largish disk where you
# want to store MFCC features.

root=/home/samuel/wsj-pf-data
data=$root/data
exp=$root/exp
x=speed_train
mfccdir=$root/mfccs/mfccdir/augmented
train=$data/pf/$x
augmented=$data/augmented-train-wsj-pf
 
data=/home/samf/Documents/art_data/kaldi_art_8

steps/make_mfcc.sh --cmd "$train_cmd" --nj 1 \
  $data exp/make_mfcc/art_data /home/samf/Documents/art_data/mfccs || exit 1;
 steps/compute_cmvn_stats.sh $data exp/make_mfcc/art_data /home/samf/Documents/art_data/mfccs || exit 1;
