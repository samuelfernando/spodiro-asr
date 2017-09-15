import re
from datetime import datetime, timedelta
from os.path import join
from readers import read_controls, read_dialogue, read_asr

dial_in = "/home/samf/museum_log/24_03_2016/stdout/stdout_24_03_2016_10_15_56.569.log"
asr_root = "/home/samf/museum_speech"
out = open("rel_procced.txt", "w")
asr_in = join(asr_root,"24_03_2016/stdouts/24_03_2016_10_13_30.txt")
#control_in = join(asr_root, "24_03_2016/controls/24_03_2016_10_15_22.control.txt")

#read_controls(join(asr_root, "24_03_2016/controls"))
#control_init, read_back = read_control(control_in)
robot_start = read_dialogue(dial_in)
asr_robot_start, asr_robot_end, asr_input = read_asr(asr_in)

controls = read_controls(join(asr_root, "24_03_2016/controls"))
control_list = sorted(controls.keys())

asr_list = list(asr_input.keys())
asr_end_list = list(asr_robot_end.keys())

def conv(dt):
	return str(dt.total_seconds())

count = 0
end_count = 0
read_count = 0
control_count = 0
prev_end  = timedelta(0,0,0)

base = control_list[control_count]
control_init, read_back = controls[base]
read_list = list(read_back.keys())
new_control_init = control_init



out.write("Base\t"+base+"\n")
	
for key in robot_start:
	htime = asr_robot_start[key]
	d,utt = robot_start[key]
	
	if end_count < len(asr_end_list):
		end_time = asr_robot_end[asr_end_list[end_count]]
		if end_time < htime:
			out.write(conv(end_time-control_init)+"\tEnd of robot speech\n")
			prev_end = end_time
			end_count+=1
			if control_init != new_control_init:
				control_init = new_control_init
				out.write("Base\t"+base+"\n")

	if read_count < len(read_list):
		read_time, num = read_back[read_list[read_count]]
		if read_time < htime:
			num = float(num)/16000
			out.write(conv(read_time-control_init)+"\tRead back\t"+str(num)+"\n")
			read_count+=1
			
	elif control_count < len(control_list)-1:
		control_count+=1
		read_count = 0
		base = control_list[control_count]
		new_control_init, read_back = controls[base]
		read_list = list(read_back.keys())
		
	if count < len(asr_list):
		time,h_utt = asr_input[asr_list[count]]
		while time < htime and count < len(asr_list):
			out.write(conv(time-control_init)+"\tASR decoded\t"+h_utt+"\t"+str(time-prev_end)+"\n")
			count+=1
			if count < len(asr_list):
				time,h_utt = asr_input[asr_list[count]]
				
	out.write(conv(htime-control_init)+"\tRobot speech\t"+utt+"\n")		
	


		
			
	
				
