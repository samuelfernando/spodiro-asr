import re
from datetime import datetime, timedelta
from os import listdir
from os.path import join


glob_pat = re.compile("(\S+) (.*)")
dial_date_pat = re.compile("(\d+)_(\d+)_(\d+)_(\d+)_(\d+)_(\d+)\.(\d+)")
asr_date_pat = re.compile("(\d+)-(\d+)-(\d+)-(\d+):(\d+):(\d+):(\d+)")
date_pat = re.compile("(\d+-\d+-\d+-\d+:\d+:\d+:\d+) (.*)")	
lm_pat = re.compile("Yarp message lm_change (\S+) (\d+) received")

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
		

def read_control(base, control_in_name, events):
	control_in = open(control_in_name)
	read_back_pat = re.compile("Read back (\d+)")
	first_read = True
	for line in control_in.readlines():
		m = glob_pat.match(line)
		if m:
			date = m.group(1)
			stuff = m.group(2)
			time = makedt(date, "asr")
			out_str = ""
			if first_read:
				out_str = "Control init "+base+" "
				first_read = False
			n = read_back_pat.match(stuff)
			if n:
				num = int(n.group(1))
				out_str = "Read back "+str(num)
			else:
				start, end, listen = stuff.strip().split(" ")
				size = int(end)-int(start)
				out_str += "Chunk "+str(size)+" "+listen
			events[time] = out_str.strip()	
	return events

def read_controls(folder_name, events):
	files = sorted(listdir(folder_name))
	for filename in files:
		base,controltmp,ext = filename.split(".")
		events = read_control(base, join(folder_name, filename), events)
	return events


	
def read_asr(asr_in_name, events):
	asr_in = open(asr_in_name)
	asr_found = False
	for line in asr_in.readlines():
		line = line.strip()
		
		m = date_pat.match(line)
		if m:
			date = m.group(1)
			time = makedt(date, "asr")
		
			v = m.group(2)	
			#if v=="Yarp message button_control start_test received":
			#	events[time] = "START_TEST"
			#if v=="Yarp message button_control new_person received":
			#	events[time] = "NEW_PERSON"
			#if v=="Yarp message speech_event start_of_speech received" or v=="Yarp message speech_override timeout received":
			#	events[time] = "robot_start_speech"
			#if v=="Yarp message speech_override start_listen received":
			#	events[time] = "start_listen"
			#if v=="Yarp message speech_override end_listen received": 
			#	events[time] = "end_listen"
			#if v=="Making new SingleUttDecoder" or v=="Endpoint so Nnet Finish decoding":		
			#	asr_found = True
			#elif asr_found:
			#	if v!="LM ready so Nnet Advance decoding":
			#		events[time] = "asr_input "+v
			#	asr_found = False
			#if v=="Yarp message speech_event SPEECH_END received":
			#	events[time] = "robot_end_speech"
			m = lm_pat.match(v)
			if m:
				lm_type = m.group(1)
				lm_num = m.group(2)
				events[time] = "lm "+lm_type+" "+lm_num
	return events




		


