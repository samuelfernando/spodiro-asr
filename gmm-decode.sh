#!/bin/bash

stage=0
nj=1
cmd=run.pl
max_active=7000
beam=13.0
lattice_beam=6.0
acwt=0.083333 # note: only really affects adaptation and pruning (scoring is on
              # lattices).
per_utt=false
do_endpointing=true
do_speex_compressing=false
scoring_opts=
skip_scoring=false

#echo "$0 $@"
. utils/parse_options.sh || exit 1;

if [ $# != 8 ]; then
echo "$#"
   echo "Usage: $0 [options] <graph-dir> <data-dir> <decode-dir>"
   echo "... where <decode-dir> is assumed to be a sub-directory of the directory"
   echo " where the models are, as prepared by steps/online/prepare_online_decoding.sh"
   echo "e.g.: $0 exp/tri3b/graph data/test exp/tri3b_online/decode/"
   echo ""
   echo ""
   echo "main options (for others, see top of script file)"
   echo "  --config <config-file>                           # config containing options"
   echo "  --nj <nj>                                        # number of parallel jobs"
   echo "  --cmd (utils/run.pl|utils/queue.pl <queue opts>) # how to run jobs."
   echo "  --acwt <float>                                   # acoustic scale used for lattice generation "
   echo "  --per-utt <true|false>                           # If true, decode per utterance without"
   echo "                                                   # carrying forward adaptation info from previous"
   echo "                                                   # utterances of each speaker."
   echo "  --scoring-opts <string>                          # options to local/score.sh"
   exit 1;
fi

graphdir=$1
dir=$2
source=$3
output_path=$4
keyphrase=$5
record_wav=$6
read_pipe=$7
should_listen=$8
decoder=gmm

#echo "platform = $platform"  

srcdir=$dir

#echo "srcdir=$srcdir graphdir=$graphdir"

for f in $srcdir/conf/online_decoding.conf $graphdir/HCLG.fst $graphdir/words.txt; do
  if [ ! -f $f ]; then
    echo "$0: no such file $f"
    exit 1;
  fi
done

#wav_rspecifier="scp:$data/wav.scp"
wav_rspecifier="scp:wav.scp"
lat_wspecifier="ark:|gzip -c > $dir/lat.1.gz" 
utt=testing

args=($utt $source $output_path $keyphrase $record_wav $read_pipe $should_listen $decoder);

new-buffer-src/simulator --do-endpointing=$do_endpointing \
   --config=$srcdir/conf/online_decoding.conf \
   --max-active=$max_active --beam=$beam --lattice-beam=$lattice_beam \
   --acoustic-scale=$acwt --word-symbol-table=$graphdir/words.txt \
     $graphdir/HCLG.fst "$wav_rspecifier" "$lat_wspecifier" ${args[@]} || exit 1;
exit 0;

#src/sf-controller --do-endpointing=$do_endpointing \
#   --config=$srcdir/conf/online_decoding.conf \
#   --max-active=$max_active --beam=$beam --lattice-beam=$lattice_beam \
#   --acoustic-scale=$acwt --word-symbol-table=$graphdir/words.txt \
#     $graphdir/HCLG.fst "$wav_rspecifier" "$lat_wspecifier" ${args[@]} || exit 1;
#exit 0;

#new-src/new-sf-controller --do-endpointing=$do_endpointing \
#   --config=$srcdir/conf/online_decoding.conf \
#   --max-active=$max_active --beam=$beam --lattice-beam=$lattice_beam \
#   --acoustic-scale=$acwt --word-symbol-table=$graphdir/words.txt \
#     $graphdir/HCLG.fst "$wav_rspecifier" "$lat_wspecifier" ${args[@]} || exit 1;
#exit 0;
