from os.path import join
import re

root = "/home/samuel/wsj-pf-data/data/balanced"

f = open(join(root, "orig", "utt2spk"))
pat = re.compile("(\S+) .*")

lines = f.readlines()

spks = {}
valid_utts = {}
total_utts = 0

for line in lines:
	line = line.strip()
	utt, spk = line.split(" ")
	if spk.startswith("c"):
		total_utts+=1
	if spk.startswith("c2"):
		valid_utts[utt] = 1
		
print(len(valid_utts), total_utts, total_utts-len(valid_utts))


def proc(filename):
	infile = open(join(root, "orig", filename))
	outfile = open(join(root, filename), "w")

	for line in infile.readlines():
		line = line.strip()
		m = pat.match(line)
		if m:
			utt = m.group(1)
			if utt.startswith("c"):
				if utt.startswith("c2"):
					outfile.write(line+"\n")
			else:
				outfile.write(line+"\n")

filenames = ["segments", "text", "wav.scp", "feats.scp", "cmvn.scp", "utt2spk"]

for filename in filenames:
	proc(filename)

