from os import listdir
from os.path import isfile, join, splitext
import re
import shutil

path="carfield_24Feb16"

files = [f for f in listdir(join(path,"text")) if isfile(join(path, "text", f))]



text_pat = re.compile("(\S+) (\S+) (.+)")

def conv(basename):
	#print("Converting ",basename)
	outname = basename.replace(":", "_")
	outname = outname.replace("-", "_")
	return outname
	
def process(base, start_points, end_points, end_text):
	#if base!="24-02-2016-09:09:45":
	#	return
	print(base)
	#for start_point in start_points:
	#	out.write("Start "+str(start_point)+"\n")
	#for end_point in end_points:
	#	out.write("End "+str(end_point)+"\n")
	if len(end_points)>0:
		header_file = open("header.txt")
		for line in header_file.readlines():
			out.write(line)
		j = 0
		for i in range(0, len(start_points)):
			if j==len(end_points):
				break			
			start = start_points[i]
			if i+1<len(start_points):
				next = start_points[i+1]
			else:
				next = 1000000000
			end = end_points[j]
			while end<next and j<len(end_points):
				text = end_text[end]
				out.write(base+".wav\t0\t"+str(start/16000)+"\t"+ str(end/16000)+ "\tspeaker1\tunknown\tnative\t"+text+"\t0\t0\t"+str(j)+"\t\t\n")
				start = end
				j = j+1
				if j==len(end_points):
					break
				end = end_points[j]
			
	
for f in files:
	base, ext = splitext(f)

	control_path = join(path, "controls", base+".control.txt")
	
	if (isfile(control_path)):
		
		#print("Found "+control_path)
		out_base = conv(base)
		src_wav = join(path, "speech", base+".wav")
		target_wav = join(path, "renamed", out_base+".wav")
		
		#print(src_wav, target_wav)
		#shutil.copyfile(src_wav, target_wav)
		
		out = open(join(path, "tdf_out", out_base+".tdf"), "w")
	
		#print("Conv "+out_base)
		start_points = []
		control_file = open(control_path)
		prev_switch=0
		for line in control_file.readlines():
			time, start, end, switch = line.strip().split(" ")
			if int(switch)==1 and prev_switch==0:
				start_points.append(float(start))
				#out.write("Start at "+start+"\n")
			prev_switch = int(switch)
		
		text_path = join(path, "text", f)
		text_file = open(text_path)
		end_points = []
		end_text = {}
		for line in text_file.readlines():
			m = text_pat.match(line.strip())
			if m:
				time = m.group(1)
				end = m.group(2)
				text = m.group(3)
				end_points.append(float(end))
				end_text[float(end)] = text
				
				
		process(out_base, start_points, end_points, end_text)
		
			
	
#	else:
		#print("Not found "+control_path)
	
#files = [f for f in listdir(join(path,"controls")) if isfile(join(path, "controls", f))]
#
#for f in files:
#	base, ext = splitext(f)
#	base = splitext(base)[0]
#	text_path = join(path, "text", base+".txt")
#	if (isfile(text_path)):
#		print("Found "+text_path)
#		#text_file = open(text_path)	
#	else:
#		print("Not found "+path)
#