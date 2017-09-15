from datetime import datetime
import re


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
			control_init = dt_conv(year,month,day,hour,minute,second,microsecond)
			base = m.group(1)
			print(base)
		if control_init!=None:
			dt = dt_conv(year,month,day,hour,minute,second,microsecond)
			td = dt - control_init
			sec = float(td.seconds)+float(td.microseconds)/1000000
			print(str(sec)+"\t"+info)
		
load_events()
