#!/bin/bash

. path.sh || exit 1;

#touch path.test
if [ $KALDI_ROOT = "/path/to/kaldi" ]; then
	echo "Must set KALDI_ROOT in path.sh to point to Kaldi install location";
	exit 0;
fi

if [  -f $KALDI_ROOT/src/kaldi.mk ]; then
	cp $KALDI_ROOT/src/kaldi.mk .
	cp $KALDI_ROOT/src/makefiles/default_rules.mk .	
else
	echo "KALDI_ROOT/src/kaldi.mk not found, please set path correctly.";
	exit 0;
fi

echo "KALDI_ROOT=$KALDI_ROOT" > path.mk

sed -i.bak 's/-I\.\./-I$(KALDI_ROOT)\/src/g' kaldi.mk


