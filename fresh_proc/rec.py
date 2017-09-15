from asr_reader import read_asr, read_controls
from os import listdir
from os.path import join, isfile


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
			
def test_asr(dirname, day):
	#global asr_robot_start, asr_robot_end, asr_input, controls
	asr_dir = join(asr_root,day, "stdouts")
	print(asr_dir)
	files = sorted(listdir(asr_dir))
	asr_robot_start, asr_robot_end, asr_input = [], [], []
	for filename in files:
		asr_in = join(asr_dir, filename)
		if isfile(asr_in):
			print(filename)
			lasr_robot_start, lasr_robot_end, lasr_input = read_asr(asr_in)
			asr_robot_start.extend(lasr_robot_start) 
			asr_robot_end.extend(lasr_robot_end)
			asr_input.extend(lasr_input)
		
	my_print("ASR Robot start", asr_robot_start)
	print(len(asr_robot_start))
	my_print("ASR Robot end", asr_robot_end)
	print(len(asr_robot_end))
	my_print("ASR input", asr_input)
	print(len(asr_input))
	
	control_dir = join(asr_root,day, "controls")
	print(control_dir)
	controls = read_controls(control_dir)
	my_print("Controls", controls)
	print(len(controls))
	return asr_robot_start, asr_robot_end, asr_input, controls

def conv(dt):
	return str(dt.total_seconds())
	
asr_root = "/home/samf/museum_speech/speech_logs"
day = "19_03_2016"
asr_robot_start, asr_robot_end, asr_input, controls = test_asr(asr_root, day)

asr_count = 0
end_count = 0
read_count = 0
control_count = 0
control_list = sorted(controls.keys())

base = control_list[control_count]
control_init, read_back = controls[base]
#read_list = list(read_back.keys())
new_control_init = control_init

out = open("rel_procced.txt", "w")
out.write("Base\t"+base+"\n")

test_mode = False

for count in range(0, len(asr_robot_start)):
	
	
	htime = asr_robot_start[count]
	if htime=="ERROR":
		continue
	elif htime=="TEST_ON":
		test_mode = True
	elif htime=="TEST_OFF":
		test_mode = False
		continue
		
	if test_mode:
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
	
