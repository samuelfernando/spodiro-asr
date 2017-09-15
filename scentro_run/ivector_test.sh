. cmd.sh
. ./path.sh
. ./utils/parse_options.sh

steps/online/nnet2/extract_ivectors_online.sh --cmd "$train_cmd" --nj 30 \
    ${train}_hires_max2 $exp/nnet2_online/extractor $exp/nnet2_online/ivectors_$
fi

