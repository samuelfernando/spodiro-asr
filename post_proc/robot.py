from os import listdir
from os.path import isfile, join, splitext
import re
import shutil

path="carfield_24Feb16"

files = [f for f in listdir(join(path,"controls")) if isfile(join(path, "controls", f))]

for f in files:
	base, ext = splitext(f)
	base = splitext(base)[0]
	print(base)
	control_path = join(path, "controls", f)
	out = open(join(path, "robot_gold", base+".tdf"), "w")
	start_points = []
	control_file = open(control_path)
	prev_switch=1
	for line in control_file.readlines():
		time, start, end, switch = line.strip().split(" ")
		if int(switch)==0 and prev_switch==1:
			start_points.append(float(start))
			prev_switch = int(switch)
		
	