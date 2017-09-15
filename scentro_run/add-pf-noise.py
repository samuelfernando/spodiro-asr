from subprocess import call, check_output
from os import listdir
from os.path import isfile, join, splitext
import re
import random

src = "/data/ac1ssf/pf-star-joined/audio-all/16kHz/train"
noise = "/home/ac1ssf/data/background/CHiME3/data/audio/16kHz/backgrounds"
noise_trim ="/data/ac1ssf/pf-star-noise/audio-noise/16kHz/train"
mix_dir = "/fastdata/ac1ssf/noisy-pf/train"
noise_length = {}

def get_rand_noise_file():
	num_files = len(noise_length)
	ar = noise_length.keys()
	rand = random.randrange(0, num_files)
	return ar[rand]

def get_rand_offset(filename, duration):
	length = noise_length[filename]
	maximum = length - duration
	rand = random.uniform(0, maximum)
	return rand
	
def get_duration(filename):
	out = check_output(["soxi", "-D", filename])
	out = out.rstrip()
	return float(out)

def make_noise(src_file, noise_file, offset, duration):
	full_noise = join(noise, noise_file)
	out_file = "noise-"+src_file
	out = join(noise_trim, out_file)
	call(["sox", full_noise, out, "trim", str(offset), str(duration)])
	return out_file

def get_noise_lengths():
	onlyfiles = [ f for f in listdir(noise) if isfile(join(noise,f)) and splitext(f)[1]==".wav" ]
	for filename in onlyfiles:
		duration = get_duration(join(noise,filename))
		noise_length[filename] = duration

def make_wsj_noise():
	onlyfiles = [ f for f in listdir(wsj_src) if isfile(join(wsj_src,f)) and splitext(f)[1]==".wav" ]
	for filename in onlyfiles:
		duration = get_duration(join(wsj_src,filename))
		rand_noise_file = get_rand_noise_file()
		rand_offset = get_rand_offset(rand_noise_file, duration)
		noise_duration = noise_length[rand_noise_file]
		#print(rand_noise_file, rand_offset, duration, noise_duration)
		rand_noise_out = make_noise(filename, rand_noise_file, rand_offset, duration)
		print("out ", rand_noise_out)

def make_pf_noise():
	onlyfiles = [ f for f in listdir(src) if isfile(join(src,f)) and splitext(f)[1]==".wav" ]
	for filename in onlyfiles:
		duration = get_duration(join(src,filename))
		rand_noise_file = get_rand_noise_file()
		rand_offset = get_rand_offset(rand_noise_file, duration)
		noise_duration = noise_length[rand_noise_file]
		#print(rand_noise_file, rand_offset, duration, noise_duration)
		rand_noise_out = make_noise(filename, rand_noise_file, rand_offset, duration)
		print("out ", rand_noise_out)

def mix_pf_noise(level, target_dir):
	onlyfiles = [ f for f in listdir(src) if isfile(join(src,f)) and splitext(f)[1]==".wav" ]
	for filename in onlyfiles:
		src_file = join(src,filename)
		noise_file = join(noise_trim,"noise-"+filename)
		#out_file = join(mix_dir, target_dir, "mix-"+target_dir+"-"+filename)
		out_file = join(mix_dir, target_dir, filename+"-"+target_dir)
		
		print(src_file)
		print(noise_file)
		print(out_file)
		call(["sox", "-m", src_file, "-v", str(level), noise_file, out_file])
		
#get_noise_lengths()
#make_wsj_noise()

#make_pf_noise()
#mix_pf_noise(0.5623413252, "5dB")
mix_pf_noise(0.316227766, "10dB")
mix_pf_noise(0.1, "20dB")
#mix_pf_noise(0.05)

#mixed = mix(rand_noise_out, filename)
	
	#print(filename, duration)
	
#call(["sox", old, "-r 16000", new, "remix", "1"])



#onlyfiles = [ f for f in listdir(noise) if isfile(join(noise,f)) and splitext(f)[1]==".wav" ]
#for filename in onlyfiles:
#	print(filename)

	




#onlyfiles = [ f for f in listdir(src) if isfile(join(src,f)) and splitext(f)[1]==".wav" ]
#for filename in onlyfiles:
#	print(filename)
	#call(["sox", old, "-r 16000", new, "remix", "1"])


	

