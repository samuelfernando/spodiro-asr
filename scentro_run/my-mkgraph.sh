#!/bin/bash

. cmd.sh
#. ./path.sh
#. ./utils/parse_options.sh

root=/home/samuel/museum-data
#lang=$root/healthy_living_lang
#lang=$root/wsj-pfstar-with-museum-filtered
#lang=$root/wsj-pfstar-with-museum


#lang=$root/fisher_bigram_filtered

lang_name=wsj-pfstar-with-museum
lang=$root/$lang_name

#graph=$root/healthy_graph
model=/home/samuel/wsj-pf-data/exp_augmented/tri4a
graph=$model/${lang_name}_graph
rm -rf $graph
utils/mkgraph.sh $lang $model $graph

