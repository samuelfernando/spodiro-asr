import re
from datetime import datetime, timedelta
from os import listdir
from os.path import join




glob_pat = re.compile("(\S+) (.*)")
dial_date_pat = re.compile("(\d+)_(\d+)_(\d+)_(\d+)_(\d+)_(\d+)\.(\d+)")
asr_date_pat = re.compile("(\d+)-(\d+)-(\d+)-(\d+):(\d+):(\d+):(\d+)")
	

def makedt(date, typename):
	if typename=="dial":
		m = dial_date_pat.match(date)
	elif typename=="asr":
		m = asr_date_pat.match(date)
	if m:
		(day, month, year, hour, minute, second, milli) = m.groups()
		
		dt = datetime(int(year), int(month), int(day), 
			int(hour), int(minute), int(second), int(milli)*1000)
		return dt



		
def read_control(control_in_name):
	control_in = open(control_in_name)
	count=0
	read_back_pat = re.compile("Read back (\d+)")
	control_init = timedelta(1979,10,4)
	read_back = {}
	first_read = False
	for line in control_in.readlines():
		m = glob_pat.match(line)
		if m:
			date = m.group(1)
			stuff = m.group(2)
			time = makedt(date, "asr")
			if not first_read:
				control_init = time
				first_read = True
			n = read_back_pat.match(stuff)
			if n:
				num = int(n.group(1))
				read_back[count] = (time, num)
				count+=1
	return control_init, read_back

def read_controls(folder_name):
	files = sorted(listdir(folder_name))
	controls = {}
	for filename in files:
		base,controltmp,ext = filename.split(".")
		controls[base] = read_control(join(folder_name, filename))
	return controls
		#print(filename)
def read_dialogue(dial_in_name):
	dial_in = open(dial_in_name)
	dial_pat = re.compile("(\S+) GenBehaviour execute \[.*speak.*\] \[([^\]]+)\]")
	count=0
	dial_init = timedelta(1979,10,4)
	robot_start = {}
	for line in dial_in.readlines():
		line = line.strip()
		m = dial_pat.match(line)
		if m:
			date = m.group(1)
			utt = m.group(2)
			time = makedt(date, "dial")
			if count==0:
				dial_init = time
	
			robot_start[count] = {}
			robot_start[count] = (time, utt)
			
			
			count+=1
	return robot_start
	

def read_asr(asr_in_name):
	asr_in = open(asr_in_name)
	time_pat = re.compile("(\S+) Yarp message speech_override timeout received")
	end_pat = re.compile("(\S+) Yarp message speech_event SPEECH_END received")
	asr_in_pat = re.compile("(\S+) Endpoint so Nnet Finish decoding")
	asr_pat = re.compile("(\S+) Yarp message speech_event start_of_speech received")
	count=0
	asr_robot_start = {}
	asr_input = {}
	asr_init = datetime(1979,10,4)
	asr_in_count = 0
	
	asr_found = False
	asr_robot_end = {}
	asr_robot_end_count = 0
	
	for line in asr_in.readlines():
		line = line.strip()
		m = asr_pat.match(line)
		if not m:
			m = time_pat.match(line)
	
		if m:
			date = m.group(1)
			time = makedt(date, "asr")
			if count==0:
				asr_init = time
			asr_robot_start[count] = time
			
			count+=1			
		m = asr_in_pat.match(line)
		if m and not asr_found:
			
			asr_in_count+=1
			asr_found = True
		elif asr_found:
			m = glob_pat.match(line)
			if m:
				time = makedt(m.group(1), "asr")
				utt = m.group(2)
				asr_input[asr_in_count] = (time, utt) 
				asr_found = False
		
		m = end_pat.match(line)
		if m:	
			time = makedt(m.group(1), "asr")
			asr_robot_end[asr_robot_end_count] = time
			asr_robot_end_count+=1
		
		
	return asr_robot_start, asr_robot_end, asr_input
	
		


