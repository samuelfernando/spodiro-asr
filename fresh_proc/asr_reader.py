import re
from datetime import datetime, timedelta
from os import listdir
from os.path import join
from sortedcontainers import SortedDict

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
	#count=0
	read_back_pat = re.compile("Read back (\d+)")
	control_init = timedelta(1979,10,4)
	read_back = []
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
				read_back.append((time, num))
				#count+=1
	return control_init, read_back

def read_controls(folder_name):
	controls = {}
	files = sorted(listdir(folder_name))
	for filename in files:
		base,controltmp,ext = filename.split(".")
		controls[base] = read_control(join(folder_name, filename))
	return controls
	
	
def read_asr(asr_in_name):
	asr_in = open(asr_in_name)
	time_pat = re.compile("(\S+) Yarp message speech_override timeout received")
	end_pat = re.compile("(\S+) Yarp message speech_event SPEECH_END received")
	asr_in_pat = re.compile("(\S+) Endpoint so Nnet Finish decoding")
	asr_old_in_pat = re.compile("(\S+) Making new SingleUttDecoder")
	asr_pat = re.compile("(\S+) Yarp message speech_event start_of_speech received")
	new_person = re.compile("(\S+) Yarp message button_control new_person received")
	new_test = re.compile("(\S+) Yarp message button_control start_test received")	
#count=0

	asr_init = datetime(1979,10,4)
	#asr_in_count = 0
	
	asr_found = False
	asr_robot_start, asr_robot_end, asr_input = [], [], []
	#asr_robot_end_count = 0
	
	for line in asr_in.readlines():
		line = line.strip()
		
		m = new_person.match(line)
		if m:
			#print("Test mode off")
			asr_robot_start.append("TEST_ON")
		m = new_test.match(line)
		if m:
			#print("Test mode on")
			test_mode = True
			asr_robot_start.append("TEST_OFF")
			
			
		
		m = asr_pat.match(line)
		if not m:
			m = time_pat.match(line)
		if m:
			date = m.group(1)
			time = makedt(date, "asr")
			#if count==0:
			#	asr_init = time
			asr_robot_start.append(time)
			
			#count+=1			
		m = asr_in_pat.match(line)
		n = asr_old_in_pat.match(line)
		if (m or n) and not asr_found:
			#asr_in_count+=1
			asr_found = True
		elif asr_found:
			m = glob_pat.match(line)
			if m:
				time = makedt(m.group(1), "asr")
				utt = m.group(2)
				#asr_input[asr_in_count] = (time, utt) 
				asr_input.append((time,utt))
				asr_found = False
		
		m = end_pat.match(line)
		if m:	
			time = makedt(m.group(1), "asr")
			#asr_robot_end[asr_robot_end_count] = time
			#asr_robot_end_count+=1
			asr_robot_end.append(time)
		if "KALDI_ASSERT" in line or "Segmentation fault" in line:
			asr_robot_start.append("ERROR")
			return asr_robot_start, asr_robot_end, asr_input
	
		
		
				
	
	#asr_robot_start.append("END_OF_FILE")
	return asr_robot_start, asr_robot_end, asr_input





		


