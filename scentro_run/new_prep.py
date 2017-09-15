from os.path import join, exists
from os import mkdir
import re

pat = re.compile("(\S+) (.*)")

new_audio = "/home/samuel/wsj-pf-data/audio/noisy-pf/speed_train"
root = "/home/samuel/wsj-pf-data/data/pf"
wav_file_in = open(join(root, "train", "wav.scp"))
if not exists(join(root, "speed_train")):
	mkdir(join(root, "speed_train"))
	
wav_file_out = open(join(root, "speed_train", "wav.scp.unsorted"), "w")



for line in wav_file_in.readlines():
	line = line.strip()
	m = pat.match(line)
	if m:
		rec_id = m.group(1)
		fields = rec_id.split("-")
		level = fields[len(fields)-1]
		if not level=="noisy":
			new_wav_0_9 = join(new_audio, "0.9", level, rec_id+"-0.9.wav")
			new_wav_1_1 = join(new_audio, "1.1", level, rec_id+"-1.1.wav")
			wav_file_out.write(rec_id+"-0.9 "+new_wav_0_9+"\n")
			wav_file_out.write(rec_id+"-1.1 "+new_wav_1_1+"\n")
			


text_file_in = open(join(root, "train", "text"))
text_file_out = open(join(root, "speed_train", "text.unsorted"), "w")
texts = {}
for line in text_file_in.readlines():
        line = line.strip()
        m = pat.match(line)
        if m:
                texts[m.group(1)] = m.group(2)

spk_file_in = open(join(root, "train", "utt2spk"))
spk_file_out = open(join(root, "speed_train", "utt2spk.unsorted"), "w")
spks = {}
for line in spk_file_in.readlines():
        line = line.strip()
        m = pat.match(line)
        if m:
                spks[m.group(1)] = m.group(2)

seg_file_in = open(join(root, "train", "segments"))
seg_file_out = open(join(root, "speed_train", "segments.unsorted"), "w")

for line in seg_file_in.readlines():
	line = line.strip()
	utt_id, rec_id, start, end = line.split(" ")
	pf1, pf2, mic, level, start, end = utt_id.split("-")
	start9 = str(float(start)/0.9)
	end9 = str(float(end)/0.9)
	start11 = str(float(start)/1.1)
	end11 = str(float(end)/1.1)
	new_utt_id9 = pf1+"-"+pf2+"-"+mic+"-"+level+"-0.9-"+start9+"-"+end9
	new_utt_id11 = pf1 +"-"+pf2+"-"+mic+"-"+level+"-1.1-"+start11+"-"+end11
	
	if not level=="noisy":
		seg_file_out.write(new_utt_id9+" "+rec_id+"-0.9 "+start9+" "+end9+"\n")
		seg_file_out.write(new_utt_id11+" "+rec_id+"-1.1 "+start11+" " +end11+"\n")
		text_file_out.write(new_utt_id9+" "+texts[utt_id]+"\n")
		text_file_out.write(new_utt_id11+" "+texts[utt_id]+"\n")
	
		spk_file_out.write(new_utt_id9+" "+spks[utt_id]+"\n")
		spk_file_out.write(new_utt_id11+" "+spks[utt_id]+"\n")

			
#	seg_file_out.write(pf1+" "+pf2+" "+mic+" "+level+" "+start+" "+end+"\n")
	

