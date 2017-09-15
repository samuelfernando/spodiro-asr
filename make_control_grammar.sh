#!/bin/bash

#. path_config.sh || exit 1;

./batch_grammar.sh controls 1

if [ ! -f fst_config_gen.txt ]; then
	touch fst_config_gen.txt
fi

if ! grep -q "controls" fst_config_gen.txt ; then
	echo "controls	1" >> fst_config_gen.txt
fi


