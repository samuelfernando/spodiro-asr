from os import listdir
from os.path import isfile, join, splitext
import re
import shutil

path="../speech-out/carfield_24Feb16/annotations_carfield"

auto_files = [f for f in listdir(join(path,"auto")) if isfile(join(path, "auto", f))]
gold_files = [f for f in listdir(join(path,"gold")) if isfile(join(path, "gold", f))]
#text_pat = re.compile("(\S+) (\S+) (.+)")

gold_pat = re.compile("gold_(.*)")

errors={}
correct=0
wrong=0
files=0

def read(name, store):
	local={}
	g = open(join(path,name, store))
	base, ext = splitext(store)
	#print(base, ext)
	for line in g.readlines():
		line = line.strip()
		#print(line)
		if name=="gold":
			m = gold_pat.match(base)
			if m:
				base = m.group(1)
		if base in line:
			#print(line)
			split = line.split("\t")
			start = split[2]
			end = split[3]
			text = split[7]
			#print(start,end,text)
			key=start+"_"+end
			#print("adding", key)
			local[key] = text
	return local
	
def proc(gold, auto):
	global correct, wrong, files, errors
	files=files+1
	local_wrong=0
	local_correct=0
	if True:
	#if "09_21_12" in gold:
		#print("Proc", gold, auto)
		golds = read("gold", gold)
		autos = read("auto", auto)
		for key in golds:
			if key in autos:
				#print("match",key)
				gold_text = golds[key]
				auto_text = autos[key]
				if gold_text==auto_text:
					#print("correct", gold_text, auto_text)
					local_correct+=1
				else:
					#print("wrong", gold_text, auto_text)
					local_wrong+=1
	correct+=local_correct
	wrong+=local_wrong

	if local_wrong in errors:
		errors[local_wrong]+=1				
	else:
		errors[local_wrong]=1
	
	if local_wrong>1:
		print(auto,local_wrong)
			
	
for f in gold_files:
	base, ext = splitext(f)
	if ext==".tdf":
		#print(base)
		m = gold_pat.match(base)
		if m:
			strip = m.group(1)
			auto_name = strip+".tdf"
			if auto_name in auto_files:
				proc(f, auto_name)
				
acc = float(correct) / float(correct+wrong)
print(files,correct, wrong,acc)
for key in errors:
	print(key, errors[key])
	
	
	

