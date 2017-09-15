from readers import read_controls
from os.path import join

asr_root = "/home/samf/museum_speech"
controls = read_controls(join(asr_root, "24_03_2016/controls"))

control_list = sorted(controls.keys())

for i in range(0, len(control_list)):
	base = control_list[i]
	control_init, read_back = controls[base]
	print(base,control_init)
	for key in read_back:
		time, num = read_back[key]
		print(key, time, num)
