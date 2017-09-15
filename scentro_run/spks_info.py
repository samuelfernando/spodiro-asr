from os.path import join
import re

root = "/home/samuel/wsj-pf-data/data/balanced"

f = open(join(root, "utt2spk"))

lines = f.readlines()

spks = {}

for line in lines:
	line = line.strip()
	utt, spk = line.split(" ")
	spks[spk] = 1

print(len(spks))


