from datetime import datetime, timedelta
from os import listdir
from os.path import join, isfile
import re

fluent = {}
event = {}
tdf = {}
consent = {}

tdf_pat = re.compile("(\S+) (\S+) A: (.*)")
year, month, day = 1970, 10, 4

def load_consents():
	f = open("consent_asr.txt")
	for line in f.readlines():
		consent[line.strip()] = 1
	
def load_fluents():
	f = open("/home/samf/museum_speech/fluent_accepted.txt")
	for line in f.readlines():
		base, start, end, utt = line.strip().split("\t")
		if base not in fluent:
			fluent[base] = []
		fluent[base].append((float(start),float(end),utt))

def load_tdfs():
	root = "/home/samf/museum_speech/transcriptions/Museum transcriptions"
	day = join(root, "24_03_2016", "output")
	folders = listdir(day)
	for folder in folders:
		#print(folder)
		if folder not in consent:
			#print("Ignoring "+folder)
			continue
		filename = join(day, folder, folder+".tdf.txt")
		if isfile(filename):
			f = open(filename)
			count = 0
			for line in f.readlines():
				line = line.strip()
				m = tdf_pat.match(line)
				if m:
					start, end, utt = m.groups()
					if folder not in tdf:
						tdf[folder] = []
					tdf[folder].append((float(start),float(end),utt))
				count+=1
			#print("Found "+str(count)+" lines")
		#else:
			#print(filename+" does not exist")
		

def load_events():
	f = open("rel_procced.txt")	
	base = None
	#ready_to_read_asr = False
	
	for line in f.readlines():
		fields = line.strip().split("\t")
		if fields[0] == "Base":
			base = fields[1]
			if base not in consent:
				#print("Ignoring "+base)
				continue
			#print(base)
		else:
			typename = fields[1]
			if typename == "Read back":
				#start = norm(process_read(fields[0], fields[2]))
				start = float(fields[0]) - float(fields[2])
			elif typename == "ASR decoded":
				#end = norm(dproc(fields[0]))
				end = float(fields[0])
				utt = fields[2]
				if base not in event:
					event[base] = []
				event[base].append((start, end, utt)) 	
				start = end
#load_fluents()
#load_events()

def find_closest(base, cstart, cend, cutt, event):
	best_diff = 1000
	bstart, bend, butt = None, None, None
	for start, end, utt in event:
		#diff = abs(cend-end)
		#if "13_38_48" in base:
		#	print(cstart, start)
		diff = abs(cend-end)
		if diff<best_diff:
			best_diff = diff
			bstart, bend, butt = start, end, utt
	return bstart, bend, butt, best_diff

load_consents()
load_tdfs()
load_events()
best_match = {}

print("TDF -> Event")

for base in sorted(tdf):
	if base in event:
		#print base
		for start, end, utt in tdf[base]:
			#print(start, end, utt)
			bstart, bend, butt, best_diff = find_closest(base, start, end, utt, event[base])
			#print(closest)
			if base not in best_match:
				best_match[base] = {}
			best_match[base][start] = end, bstart, bend, butt, best_diff

			#if best_diff>0.5:
				#print(start, end, utt)
				#print(bstart, bend, butt, best_diff)

best_match_rev = {}
print("Event -> TDF")

for base in sorted(event):
	if base in tdf:
		#print base
		for start, end, utt in event[base]:
			bstart, bend, butt, best_diff = find_closest(base, start, end, utt, tdf[base])
			#print(closest)
			if base not in best_match_rev:
				best_match_rev[base] = {}
			best_match_rev[base][start] = end, bstart, bend, butt, best_diff
			#if best_diff>0.5:
				#print(start, end, utt)
				#print(bstart, bend, butt, best_diff)

def normalize(utt):
	tokens = re.split(" ", utt)
	return tokens

def get_sim(asr_utt, man_utt):
	asr_norm = normalize(asr_utt)
	man_norm = normalize(man_utt)
	#print(norm1, norm2)
	
	#asr_norm = asr_utt
	#man_norm = man_utt
	total = 0
	found = 0
	for a in asr_norm:
		total+=1
		if a in man_norm:
			found+=1
	return float(found)/total

correct_count, wrong_count, disfluent = 0,0,0
match_count = 0
no_match_count = 0	
for base in sorted(best_match):
	if base in best_match_rev:
		print(base)
		#print "Match"
		
		#correct_count, wrong_count, disfluent = 0,0,0
		for start in sorted(best_match[base]):
			#print(time_id, best_match[base][time_id])
			end, bstart, bend, butt, diff = best_match[base][start] 
			#check = str(start)+"-"+str(end)
			#print(time_id, check)
			#print(start, best_match[base][start])
			if bstart in best_match_rev[base]:
				lend, rstart, rend, rutt, rdiff = best_match_rev[base][bstart]
				#print(check, rstart, rend)
				if rstart==start:
					#print "Match"
					#print("Match", start, end, butt, bstart, bend, rutt)
					match_count+=1
					if rutt==butt:
						correct_count+=1
						#print("Correct")
					else:
						res = get_sim(butt, rutt)
				#print(utt, "best match", res)
						if res >= 0.75:
							print("Disfluent",start, end, butt, bstart, bend, rutt, res) 
							disfluent+=1
						else:
							wrong_count+=1
							print("Wrong", start, end, butt, bstart, bend, rutt, res)
						#print("Wrong")
				else:
					#print("No match", start, end, butt, bstart, bend, rutt)
					no_match_count+=1
			else:
				#print("No match 2", start, end, butt, bstart, bend, rutt)
				no_match_count+=1

print(match_count, no_match_count)
print(correct_count, wrong_count, disfluent)
print("Accuracy", str(float(correct_count+disfluent)/(correct_count+wrong_count+disfluent)))
		
		#print "Rev match"
		
			#print(time_id, check)
#for base in fluent:
#	print(base)
#	for start, end, utt in fluent[base]:
#		print(start, end, utt)
#
#for base in event:
#	print(base)
#	for start, end, utt in event[base]:
#		print(start, end, utt)
