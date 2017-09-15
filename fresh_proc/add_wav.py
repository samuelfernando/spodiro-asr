from os.path import join, isfile

f = open("consent_asr.txt")
o = open("wav_consent.txt", "w")
root = "/home/samf/museum_speech/speech_logs"
	
for line in f.readlines():
	base = line.strip()
	day, month, year, hour, minute, second = base.split("_")
	day_str = day+"_"+month+"_"+year
	path = join(root, day_str, "speech", base+".wav")
	if not isfile(path):
		print("Could not find "+path)
	else:
		o.write(base+" "+path+"\n")
