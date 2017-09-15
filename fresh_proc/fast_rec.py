from fast_reader import read_asr, read_controls
from os import listdir
from os.path import join, isfile
from sortedcontainers import SortedDict

events = SortedDict()

def my_print(name,var):
	print(name)
	return
	if name=="Controls":
		print("Doing controls")
		for base in sorted(var):
			control_init, read_back = var[base]
			print("init", control_init)
			for time, num in read_back:
				print(time, num)
			print(len(read_back))
	else:
		for val in var:
			print(val)
			
def test_asr(dirname, events, day):
	asr_dir = join(asr_root,day, "stdouts")
	print(asr_dir)
	files = sorted(listdir(asr_dir))

	for filename in files:
		asr_in = join(asr_dir, filename)
		if isfile(asr_in):
			print(filename)
			events = read_asr(asr_in, events)

	
	
	control_dir = join(asr_root,day, "controls")
	print(control_dir)
	events = read_controls(control_dir, events)


def conv(dt):
	return str(dt.total_seconds())
	
asr_root = "/home/samf/museum_speech/speech_logs"

all_days = listdir(asr_root)

for day in all_days:
	print(day)
	#	proc_day(dial_root, asr_root, day)
	#day = "19_03_2016"
	test_asr(asr_root, events, day)

f = open("all_log.txt", "w")

for time in events:
#	print(time, events[time])
	out_str = ""
	out_str+=str(time.year)+"\t"
	out_str+=str(time.month)+"\t"
	out_str+=str(time.day)+"\t"
	out_str+=str(time.hour)+"\t"
	out_str+=str(time.minute)+"\t"
	out_str+=str(time.second)+"\t"
	out_str+=str(time.microsecond)+"\t"
	out_str+=str(events[time])+"\n"
	
	
	f.write(out_str)
	
