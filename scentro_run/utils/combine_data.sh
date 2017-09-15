#!/bin/bash
# Copyright 2012  Johns Hopkins University (Author: Daniel Povey).  Apache 2.0.
#           2014  David Snyder

# This script operates on a data directory, such as in data/train/.
# See http://kaldi-asr.org/doc/data_prep.html#data_prep_data
# for what these directories contain.

# Begin configuration section.
extra_files= # specify addtional files in 'src-data-dir' to merge, ex. "file1 file2 ..."
skip_fix=false # skip the fix_data_dir.sh in the end
# End configuration section.

echo "$0 $@"  # Print the command line for logging

if [ -f path.sh ]; then . ./path.sh; fi
. parse_options.sh || exit 1;

if [ $# -lt 2 ]; then
  echo "Usage: combine_data.sh [--extra-files 'file1 file2'] <dest-data-dir> <src-data-dir1> <src-data-dir2> ..."
  echo "Note, files that don't appear in first source dir will not be added even if they appear in later ones."
  exit 1
fi

dest=$1;
shift;

first_src=$1;

rm -r $dest 2>/dev/null
mkdir -p $dest;

export LC_ALL=C

for dir in $*; do
  if [ ! -f $dir/utt2spk ]; then
    echo "$0: no such file $dir/utt2spk"
    exit 1;
  fi
done

# W.r.t. utt2uniq file the script has different behavior compared to other files
# it is not compulsary for it to exist in src directories, but if it exists in
# even one it should exist in all. We will create the files where necessary
has_utt2uniq=false
for in_dir in $*; do
  if [ -f $in_dir/utt2uniq ]; then
    has_utt2uniq=true
    break
  fi
done

if $has_utt2uniq; then
  # we are going to create an utt2uniq file in the destdir
  for in_dir in $*; do
    if [ ! -f $in_dir/utt2uniq ]; then
      # we assume that utt2uniq is a one to one mapping
      cat $in_dir/utt2spk | awk '{printf("%s %s\n", $1, $1);}'
    else
      cat $in_dir/utt2uniq
    fi
  done | sort -k1 > $dest/utt2uniq
  echo "$0: combined utt2uniq"
fi
# some of the old scripts might provide utt2uniq as an extrafile, so just remove it
extra_files=$(echo "$extra_files"|sed -e "s/utt2uniq//g")

for file in utt2spk utt2lang utt2dur feats.scp text cmvn.scp segments reco2file_and_channel wav.scp spk2gender $extra_files; do
  exists_somewhere=false
  absent_somewhere=false
  for d in $*; do
    if [ -f $d/$file ]; then
      exists_somewhere=true
    else
      absent_somewhere=true
      fi
  done

  if ! $absent_somewhere; then
    set -o pipefail
    ( for f in $*; do cat $f/$file; done ) | sort -k1 > $dest/$file || exit 1;
    set +o pipefail
    echo "$0: combined $file"
  else
    if ! $exists_somewhere; then
      echo "$0 [info]: not combining $file as it does not exist"
    else
      echo "$0 [info]: **not combining $file as it does not exist everywhere**"
    fi
  fi
done

utils/utt2spk_to_spk2utt.pl <$dest/utt2spk >$dest/spk2utt

if ! $skip_fix ; then
  utils/fix_data_dir.sh $dest || exit 1;
fi

exit 0