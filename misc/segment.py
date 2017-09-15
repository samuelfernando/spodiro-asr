from subprocess import call
from os import listdir
from os.path import isfile, join, splitext
import re

root="speech-out"
#root="speech-out/carfield_24Feb16"
#root = "hri_speech"
target = join(root, "speech-segments")
src = join(root,"seg_src")
#src = join(root,"speech")

onlyfiles = [ f for f in listdir(src) if isfile(join(src,f)) and splitext(f)[1]==".wav" ]

for filename in onlyfiles:
	my_list = []
	my_str =""
	base = splitext(filename)[0]
	print(base)
	#points = open(join("speech-out/controls", base+".control.txt"))
	points = open(join(root,"controls", base+".control.txt"))
	
	lines = points.readlines()
	old = join(src, filename)
	new = join(target, filename)
	print(old, new)
	my_list.append("sox")
	my_list.append(old)
	my_list.append(new)
	my_list.append("trim")
	prev_offset = 0
	prev_listen = False
	listen = False
	
	for line in lines:
		line = line.strip()
		fields = line.split(" ")
		start = float(fields[1])/16000
		end = float(fields[2])/16000
		#start = int(fields[0])
		#end = int(fields[1])
		active = int(fields[3])
		if active==1:
			listen = True
		else:
			listen = False
		if prev_listen!=listen:
			#print(start-prev_offset)
			my_str += " "+str(start-prev_offset)
			my_list.append(str(start-prev_offset))
			prev_offset = start
			
		prev_listen = listen
		
		#print(start,end,active)
		#print(line)
	print(my_str)
	

	call(my_list)

