import re
from datetime import datetime, timedelta

dial_in = open("/home/samf/museum_log/24_03_2016/stdout/stdout_24_03_2016_10_15_56.569.log")
#dial_in = open("/home/samf/museum_log/24_03_2016/java_log/java_log_24_03_2016_10_15_56.569.txt")
#dial_out = open("robot_utts.txt", "w")


asr_in = open("/home/samf/museum_speech/24_03_2016/stdouts/24_03_2016_10_13_30.txt")
out = open("procced.txt", "w")

dial_pat = re.compile("(\S+) GenBehaviour execute \[.*speak.*\] \[([^\]]+)\]")
asr_pat = re.compile("(\S+) Yarp message speech_event start_of_speech received")
time_pat = re.compile("(\S+) Yarp message speech_override timeout received")
end_pat = re.compile("(\S+) Yarp message speech_event SPEECH_END received")
asr_in_pat = re.compile("(\S+) Endpoint so Nnet Finish decoding")
dial_date_pat = re.compile("(\d+)_(\d+)_(\d+)_(\d+)_(\d+)_(\d+)\.(\d+)")
asr_date_pat = re.compile("(\d+)-(\d+)-(\d+)-(\d+):(\d+):(\d+):(\d+)")
glob_pat = re.compile("(\S+) (.*)")
count=0
robot_start = {}

dial_init = timedelta(1979,10,4)
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

count = 0
end_count = 0

prev_end  = timedelta(0,0,0)

for key in robot_start:
	htime = asr_robot_start[key]
	d,utt = robot_start[key]
	
	if end_count < len(asr_end_list):
		end_time = asr_robot_end[asr_end_list[end_count]]
		if end_time < htime:
			out.write(str(key)+"\t"+str(end_time)+"\tEnd of robot speech (ASR)\n")
			prev_end = end_time
			end_count+=1
			
	if count < len(asr_list):
		time,h_utt = asr_input[asr_list[count]]
		while time < htime and count < len(asr_list):
			out.write(str(key)+"\t"+str(time)+"\t"+h_utt+"\t"+str(time-prev_end)+"\n")
			count+=1
			if count < len(asr_list):
				time,h_utt = asr_input[asr_list[count]]
		
			
	out.write(str(key)+"\t"+str(htime)+"\t"+str(d)+"\t"+utt+"\n")
	latency = 0
		#if d>htime:
			#print(key, htime,d, d-htime)
		#	latency = d - htime
		#else:
		#	latency = htime - d
			#print(key, htime,d, htime-d)
			
		#if latency>threshold:
		#	out.write("High latency\t"+str(key)+"\t"+str(htime)+"\t"+str(d)+"\n")

		
			
	
				
