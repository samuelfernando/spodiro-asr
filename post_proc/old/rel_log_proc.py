import re
from datetime import datetime, timedelta
from os.path import join


dial_in = open("/home/samf/museum_log/24_03_2016/stdout/stdout_24_03_2016_10_15_56.569.log")
#dial_in = open("/home/samf/museum_log/24_03_2016/java_log/java_log_24_03_2016_10_15_56.569.txt")
#dial_out = open("robot_utts.txt", "w")

asr_root = "/home/samf/museum_speech"

asr_in = open(join(asr_root,"24_03_2016/stdouts/24_03_2016_10_13_30.txt"))
control_in = open(join(asr_root, "24_03_2016/controls/24_03_2016_10_15_22.control.txt"))

out = open("rel_procced.txt", "w")

dial_pat = re.compile("(\S+) GenBehaviour execute \[.*speak.*\] \[([^\]]+)\]")
asr_pat = re.compile("(\S+) Yarp message speech_event start_of_speech received")
time_pat = re.compile("(\S+) Yarp message speech_override timeout received")
end_pat = re.compile("(\S+) Yarp message speech_event SPEECH_END received")
asr_in_pat = re.compile("(\S+) Endpoint so Nnet Finish decoding")
dial_date_pat = re.compile("(\d+)_(\d+)_(\d+)_(\d+)_(\d+)_(\d+)\.(\d+)")
asr_date_pat = re.compile("(\d+)-(\d+)-(\d+)-(\d+):(\d+):(\d+):(\d+)")
glob_pat = re.compile("(\S+) (.*)")
read_back_pat = re.compile("Read back (\d+)")


def makedt(date, typename):
	if typename=="dial":
		m = dial_date_pat.match(date)
	elif typename=="asr":
		m = asr_date_pat.match(date)
	if m:
		(day, month, year, hour, minute, second, milli) = m.groups()
		#print(day, month, year, hour, minute, second, milli) 
		dt = datetime(int(year), int(month), int(day), 
			int(hour), int(minute), int(second), int(milli)*1000)
		return dt


control_init = timedelta(1979,10,4)
#line = control_in.readline()
#m = glob_pat.match(line)
#if m:
#	date = m.group(1)
#	control_init = makedt(date, "asr")
#	
count=0
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
		#print(count, date,utt)
		#dial_out.write(str(count)+"\t"+str(rel_time)+"\t"+utt+"\n")
		count+=1
		
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
	#if not m:
	#	m = end_pat.match(line)
	if m:
		date = m.group(1)
		time = makedt(date, "asr")
		if count==0:
			asr_init = time
		asr_robot_start[count] = time
		#print(count, time)
		count+=1
			#print(line)
			
	m = asr_in_pat.match(line)
	if m and not asr_found:
		#print("ASR match", line)
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
		#print(line)
		time = makedt(m.group(1), "asr")
		asr_robot_end[asr_robot_end_count] = time
		asr_robot_end_count+=1
	#print(date,utt)
	#asr_out.write(str(count)+"\t"+str(rel_time)+"\tSpeech started\n")
    
	
		
#print("Robot utts", len(robot))
#print("Human utts", len(human))
threshold = timedelta(0,0,500000)

asr_list = list(asr_input.keys())
asr_end_list = list(asr_robot_end.keys())
read_list = list(read_back.keys())

count = 0
end_count = 0
read_count = 0

prev_end  = timedelta(0,0,0)

for key in robot_start:
	htime = asr_robot_start[key]
	d,utt = robot_start[key]
	
	if end_count < len(asr_end_list):
		end_time = asr_robot_end[asr_end_list[end_count]]
		if end_time < htime:
			out.write(str(key)+"\t"+str(end_time-control_init)+"\tEnd of robot speech (ASR)\n")
			prev_end = end_time
			end_count+=1

	if read_count < len(read_list):
		read_time, num = read_back[read_list[read_count]]
		if read_time < htime:
			num = float(num)/16000
			out.write(str(key)+"\t"+str(read_time-control_init)+"\tRead back\t"+str(num)+"\n")
			read_count+=1
			
	if count < len(asr_list):
		time,h_utt = asr_input[asr_list[count]]
		while time < htime and count < len(asr_list):
			out.write(str(key)+"\t"+str(time-control_init)+"\t"+h_utt+"\t"+str(time-prev_end)+"\n")
			count+=1
			if count < len(asr_list):
				time,h_utt = asr_input[asr_list[count]]
		
			
	#out.write(str(key)+"\t"+str(htime)+"\t"+str(d)+"\t"+utt+"\n")
	out.write(str(key)+"\t"+str(htime-control_init)+"\t"+utt+"\n")
		

#latency = 0
		#if d>htime:
			#print(key, htime,d, d-htime)
		#	latency = d - htime
		#else:
		#	latency = htime - d
			#print(key, htime,d, htime-d)
			
		#if latency>threshold:
		#	out.write("High latency\t"+str(key)+"\t"+str(htime)+"\t"+str(d)+"\n")

		
			
	
				
