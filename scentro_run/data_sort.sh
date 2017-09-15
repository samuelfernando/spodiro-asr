#!/bin/bash

srcdir=$1

cd $srcdir
 
sort -k1 wav.scp.unsorted > wav.scp
sort -k1 utt2spk.unsorted > utt2spk
sort -k1 text.unsorted > text


utt2spk_to_spk2utt.pl utt2spk > spk2utt

if [ -f "segments.unsorted" ]; then
	sort -k1 segments.unsorted > segments
fi

if [ -f "feats.scp.unsorted" ]; then
	sort -k1 feats.scp.unsorted > feats.scp
fi

if [ -f "cmvn.scp.unsorted" ]; then
	sort -k1 cmvn.scp.unsorted > cmvn.scp
fi
