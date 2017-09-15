from subprocess import call, check_output
from os import listdir, mkdir
from os.path import isfile, join, splitext, exists
import re
import random

root = "/home/samuel/wsj-pf-data/audio/noisy-pf"
noise = "/home/samuel/wsj-pf-data/audio/background_noise/CHiME3/data/audio/16kHz/backgrounds"
src = join(root, "train")
target = join(root, "speed_train")
noise_levels = ["clean", "5dB", "10dB", "20dB"]
#noise_levels = ["5dB", "10dB", "20dB"]

noise_length = {}
levels = {}
levels["5dB"] = 0.5623413252
levels["10dB"] = 0.316227766
levels["20dB"] = 0.1

count = 0

if not exists(target):
	mkdir(target)
	

def get_noise_lengths():
	onlyfiles = [ f for f in listdir(noise) if isfile(join(noise,f)) and splitext(f)[1]==".wav" ]
	for filename in onlyfiles:
		duration = get_duration(join(noise,filename))
		noise_length[filename] = duration

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


def make_noise(noise_file, offset, duration, out):
	full_noise = join(noise, noise_file)
	
	call(["sox", full_noise, out, "trim", str(offset), str(duration)])

def augment_sub(filename, speed, noise_level):
	global count
	src_file = join(src,"clean", filename)
	
	fields = splitext(filename)[0].split("-")
	noise_name = clean_name = new_name = fields[0]
	
	for i in range(1, len(fields)-1):
		noise_name = clean_name = new_name = new_name+"-"+fields[i]
	new_name+= "-"+noise_level+"-"+speed+".wav"
	
	clean_name+="-clean-"+speed+".wav"
	noise_name+="-noise-"+speed+".wav"
	noise_file = join(target, speed, "noise", noise_name)
	clean_adjusted = join(target, speed, "clean", clean_name)
	
	if not exists(join(target, speed, noise_level)):
		mkdir(join(target, speed, noise_level))
	
	target_file = join(target, speed, noise_level, new_name)
	print(src_file, target_file)
	if noise_level=="clean":
		call(["sox", src_file, clean_adjusted, "tempo", "-s", speed])
		duration = get_duration(clean_adjusted)
		rand_noise_file = get_rand_noise_file()
		rand_offset = get_rand_offset(rand_noise_file, duration)
		if not exists(join(target, speed, "noise")):
			mkdir(join(target, speed, "noise"))
		make_noise(rand_noise_file, rand_offset, duration, noise_file)
	else:
		level = levels[noise_level]
		call(["sox", "-m", clean_adjusted, "-v", str(level), noise_file, target_file])
		
	#duration = get_duration(src_file)
	#rand_noise_file = get_rand_noise_file()
	#rand_offset = get_rand_offset(rand_noise_file, duration)
	
	
#call(["sox", src_file, target_file,"tempo", "-s", speed])
	
	
def augment(filename, speed):
	if not exists(join(target, speed)):
		mkdir(join(target, speed))
		
	for noise_level in noise_levels:
		augment_sub(filename, speed, noise_level)
		
get_noise_lengths()			
onlyfiles = [ f for f in listdir(join(src,"clean")) if isfile(join(src,"clean",f)) and splitext(f)[1]==".wav" ]	
for filename in onlyfiles:
	augment(filename, "0.9")
	augment(filename, "1.1")
	

