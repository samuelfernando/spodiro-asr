#!/bin/bash

#. path_config.sh || exit 1;

python make_jsgf.py
while IFS=$'\t' read -a myArray
do
 ./batch_grammar.sh ${myArray[0]} ${myArray[1]}
done < fst_config_gen.txt


