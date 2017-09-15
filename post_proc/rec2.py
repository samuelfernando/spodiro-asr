import re
from datetime import datetime, timedelta
from os import listdir 
from os.path import join, isfile
from fast_reader import read_controls, read_dialogue, read_asr


#control_in = join(asr_root, "24_03_2016/controls/24_03_2016_10_15_22.control.txt")

#read_controls(join(asr_root, "24_03_2016/controls"))
#control_init, read_back = read_control(control_in)

robot_start, asr_robot_start, asr_robot_end, asr_input = [], [], [], []
controls = {}


def my_print(name,var):
	print(name)
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
		
	
def test_dial(dirname, day):
	global robot_start
	files = sorted(listdir(dirname))
	for filename in files:
		dial_in = join(dirname, filename)
		if isfile(dial_in):
			if day in filename:
				print(filename)
				robot_start = read_dialogue(robot_start, dial_in)
	my_print("Robot start", robot_start)
	print(len(robot_start))
def test_asr(dirname, day):
	global asr_robot_start, asr_robot_end, asr_input, controls
	asr_dir = join(asr_root,day, "stdouts")
	print(asr_dir)
	files = sorted(listdir(asr_dir))
	for filename in files:
		asr_in = join(asr_dir, filename)
		if isfile(asr_in):
			print(filename)
			asr_robot_start, asr_robot_end, asr_input = read_asr(asr_in, asr_robot_start, asr_robot_end, asr_input)
	
	my_print("ASR Robot start", asr_robot_start)
	print(len(asr_robot_start))
	my_print("ASR Robot end", asr_robot_end)
	print(len(asr_robot_end))
	my_print("ASR input", asr_input)
	print(len(asr_input))
	
	control_dir = join(asr_root,day, "controls")
	print(control_dir)
	controls = read_controls(controls, control_dir)
	my_print("Controls", controls)
	print(len(controls))
	
def proc_day(dial_root, asr_root, day):
	#dial_in = "/home/samf/museum_log/24_03_2016/stdout/stdout_24_03_2016_10_15_56.569.log"
	#dial_dir = join(dial_root, day, "stdout")
	dial_dir = dial_root
		
	test_dial(dial_dir, day)
	
	#asr_dir = join(asr_root,day, "stdouts")
	test_asr(asr_root, day)
	#exit(1)	
	
	
	
def conv(dt):
	return str(dt.total_seconds())



dial_root = "/home/samf/museum_log"
asr_root = "/home/samf/museum_speech/speech_logs"
day = "19_03_2016"

#all_days = listdir(asr_root)

#for day in all_days:
#	print(day)
#	proc_day(dial_root, asr_root, day)
proc_day(dial_root, asr_root, day)

#exit(1)

control_list = sorted(controls.keys())
	
#asr_list = list(asr_input.keys())
#asr_end_list = list(asr_robot_end.keys())


asr_count = 0
end_count = 0
read_count = 0
control_count = 0
prev_end  = timedelta(0,0,0)

base = control_list[control_count]
control_init, read_back = controls[base]
#read_list = list(read_back.keys())
new_control_init = control_init


out = open("rel_procced2.txt", "w")

out.write("Base\t"+base+"\n")
	
#for key in robot_start:
error_state = False

for count in range(0, len(robot_start)):
	
	if error_state:
		print("In error state")
		read = robot_start[count]
		if read=="END_OF_FILE":
			error_state = False
		continue
			
	htime = asr_robot_start[count]
	read = robot_start[count]
	
	if read=="END_OF_FILE":
		continue
	else:
		d,utt = read
	
	if htime=="ERROR":
		error_state = True
		continue
	
	if end_count < len(asr_robot_end):
		end_time = asr_robot_end[end_count]
		if end_time < htime:
			out.write(conv(end_time-control_init)+"\tEnd of robot speech\n")
			prev_end = end_time
			end_count+=1
			if control_init != new_control_init:
				control_init = new_control_init
				out.write("Base\t"+base+"\n")

	if read_count < len(read_back):
		read_time, num = read_back[read_count]
		if read_time < htime:
			num = float(num)/16000
			out.write(conv(read_time-control_init)+"\tRead back\t"+str(num)+"\n")
			read_count+=1
			
	elif control_count < len(control_list)-1:
		control_count+=1
		read_count = 0
		base = control_list[control_count]
		new_control_init, read_back = controls[base]
		#read_list = list(read_back.keys())
		
	if asr_count < len(asr_input):
		time,h_utt = asr_input[asr_count]
		while time < htime and asr_count < len(asr_input):
			out.write(conv(time-control_init)+"\tASR decoded\t"+h_utt+"\t"+str(time-prev_end)+"\n")
			asr_count+=1
			if asr_count < len(asr_input):
				time,h_utt = asr_input[asr_count]
	#out.write(str(htime)+"\t"+str(control_init)+"\tDebug\n")
	out.write(conv(htime-control_init)+"\tRobot speech\t"+utt+"\n")		
	


		
			
	
				
