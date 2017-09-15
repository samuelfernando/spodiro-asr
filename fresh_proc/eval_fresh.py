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
	asr_root = "/home/samf/museum_speech/speech_logs"
	all_days = listdir(asr_root)
	root = "/home/samf/museum_speech/transcriptions/Museum transcriptions"
	for day in all_days:
		#print(day)
		day_folder = join(root, day, "output")
		session_folders = listdir(day_folder)
		for session_folder in session_folders:
			#print(session_folder)
			if session_folder not in consent:
				#print("Ignoring "+folder)
				continue
			filename = join(day_folder, session_folder, session_folder+".tdf.txt")
			if isfile(filename):
				f = open(filename)
				count = 0
				for line in f.readlines():
					line = line.strip()
					m = tdf_pat.match(line)
					if m:
						start, end, utt = m.groups()
						if session_folder not in tdf:
							tdf[session_folder] = []
						tdf[session_folder].append((float(start),float(end),utt))
					count+=1
			#print("Found "+str(count)+" lines")
		#else:
			#print(filename+" does not exist")
		

def dt_conv(year,month,day,hour,minute,second,microsecond):
	return datetime(int(year),int(month),int(day),int(hour),int(minute),int(second),int(microsecond))
def load_events():
	f = open("all_log.txt")	
	base = None
	#ready_to_read_asr = False
	read_pat = re.compile("Read back (\d+)")
	control_pat = re.compile("Control init (.*)")
	asr_pat = re.compile("asr_input (.*)")
	
	base = None
	control_init = None
	for line in f.readlines():
		year,month,day,hour,minute,second,microsecond,info = line.strip().split("\t")
		m = control_pat.match(info)
		if m:
			control_init =  dt_conv(year,month,day,hour,minute,second,microsecond)
			base = m.group(1)
		m = read_pat.match(info)
		if m:		
			dt = dt_conv(year,month,day,hour,minute,second,microsecond)
			offset = float(m.group(1))*1000000/16000
			t = timedelta(0, 0, offset)
			start = dt - t
		
		m = asr_pat.match(info)
		if m:
			end = dt_conv(year,month,day,hour,minute,second,microsecond)
			utt = m.group(1)
			
			end_o = end - control_init
			start_o = (start - control_init)
			
			end_o = end_o.seconds + end_o.microseconds/1000000
			start_o = start_o.seconds + start_o.microseconds/1000000
			
			if base not in event:
				event[base] = []
			event[base].append((start_o, end_o, utt)) 	
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
