import re
from os.path import isfile, join, exists
from os import mkdir

alldialogue={}
allquestions={}
utterance_read = 0
utterance_write = 0
#root="/home/osboxes/NetBeansProjects/SpoDiRo"
sub="resource/simple_quiz"
proc_out="jsgf-dialogue/processed"
jsgf_out="jsgf-dialogue/generated_jsgfs"
fst_conf = {}
if not exists(proc_out):
	mkdir(proc_out)
	
if not exists(jsgf_out):
	mkdir(jsgf_out)
	
		
class Question:
	question=""
	explanation=""
	correctAnswerIndex=-1
	def __init__(self):
		self.answer=[]	

def read_dialogue(lines):
	global alldialogue
	global utterance_read
	#f = open(join(root,sub,base+".txt"))
	#lines = f.readlines()
	#alldialogue[base] = {}
	for line in lines:
		phrase = line.strip()
		if phrase.startswith("C:"):
			phrase = phrase[2:].strip()
			alldialogue[utterance_read] = phrase
			utterance_read+=1
		
def write_dialogue():
	global alldialogue
	out = open(join(proc_out,"dialogue.txt"), "w")			
	for utterance_no in alldialogue:
		out.write(str(utterance_no)+"\t"+alldialogue[utterance_no]+"\n")	
	
def read_questions(base, lines):
	global allquestions
#	global questionNo
#	f = open(join(root,sub,base+".txt"))
	allquestions[base]={}
#	lines = f.readlines()
	questionNo = 0	
	lines.pop(0)
#	lines.pop(0)
	count=0
	for line in lines:
		check = count % 9
		if check==0:
			question = line.strip()
			if not question.startswith("GOTO"):
				allquestions[base][questionNo] = Question()
				allquestions[base][questionNo].question = question
		elif 2<=check and check<=5:
			answer = line.strip()
			if answer.startswith("*"):
				ansNo = check-2
				allquestions[base][questionNo].correctAnswerIndex = ansNo
				answer = answer[1:].strip()
			allquestions[base][questionNo].answer.append(answer)
		elif check==7:
			explanation = line.strip()
			allquestions[base][questionNo].explanation = explanation
			questionNo+=1
		count+=1
		
		
def write_questions(name, questions):
	out = open(join(proc_out,name+".txt"), "w")
	#global allquestions
	for name in questions:
		for questionNo in questions[name]:
			q = questions[name][questionNo]
			out.write(str(questionNo)+"\tQ\t"+q.question+"\n")
			for i in range(0,4):
				if i==q.correctAnswerIndex:
					out.write(str(questionNo)+"\tA\t*"+q.answer[i]+"\n")
				else:
					out.write(str(questionNo)+"\tA\t"+q.answer[i]+"\n")
			out.write(str(questionNo)+"\tE\t"+q.explanation+"\n")


	
def write_jsgfs():
	dialogue_write = 0
	
#	conf = open("fst_config_gen.txt","w")
	if not exists(join(jsgf_out, "dialogue")):
		mkdir(join(jsgf_out,"dialogue"))

	if not exists(join(jsgf_out, "questions")):
		mkdir(join(jsgf_out,"questions"))

	for utteranceNo in alldialogue:
		phrase = alldialogue[utteranceNo]
		jsgf = open(join(jsgf_out, "dialogue", str(dialogue_write)+".jsgf"), "w")
		jsgf.write("#JSGF V1.0;\ngrammar phrase;\npublic <phrase> = !SIL | <utt> ;\n\n")
		jsgf.write("<utt> = "+re.sub(r'[^\w ]+', '', phrase.upper())+";\n")
		dialogue_write+=1
	fst_conf["dialogue"] = dialogue_write
	#conf.write("dialogue\t"+str(dialogue_write)+"\n")
	question_write = 0
	for name in allquestions:
		for questionNo in allquestions[name]:
			q = allquestions[name][questionNo]
			
			jsgf = open(join(jsgf_out, "questions", str(question_write)+".jsgf"), "w")
			jsgf.write("#JSGF V1.0;\ngrammar phrase;\npublic <phrase> = !SIL\n|<answer0>\n|<answer1>\n|<answer2>\n|<answer3>;\n\n")
			for i in range(0,4):
				jsgf.write("<answer"+str(i)+"> = "+re.sub(r'[^\w ]+', '', q.answer[i].upper())+";\n")
			question_write+=1
#	conf.write("questions\t"+str(question_write)+"\n")
	fst_conf["questions"] = question_write


def read(base):
	f = open(join(root,sub,base+".txt"))
	lines = f.readlines()
	modeline = lines.pop(0).strip()
	prefix="MODE: "
	mode = modeline[len(prefix):]
	#print(mode)
	if mode=="dialogue":
		print("Reading dialogue "+base)
		read_dialogue(lines)
		try:
			write_dialogue()
		except SyntaxError as e:
			print "Syntax error {0}".format(e.text)
	elif mode=="questions":
		print("Reading questions "+base)
		read_questions(base, lines)
		write_questions(base, allquestions)


def read_config(filename):
	conf = open(filename)
	lines = conf.readlines()
	params = {}
	for line in lines:
		fields = line.strip().split("\t")
		params[fields[0]] = fields[1]
	script_file = params["script_config_file"]
	script_conf = open(join(root, script_file))
	lines = script_conf.readlines()
	params = {}
	for line in lines:
		fields = line.strip().split("\t")
		params[fields[0]] = fields[1]		
	masterList = params["out_master_file"]		
	f = open(join(root, "resource/generated", masterList+".txt"))
	lines = f.readlines()
	for line in lines:
		read(line.strip())
		
def read_fst_config(filename):
	global fst_conf
	if not isfile(filename):
		return
	conf = open(filename)
	lines = conf.readlines()
	for line in lines:
		fields = line.strip().split("\t")
		fst_conf[fields[0]] = fields[1]
	
def write_fst_config(filename):
	global fst_conf
	conf = open(filename, "w")
	for key in fst_conf:
		conf.write(key+"\t"+str(fst_conf[key])+"\n")

def get_root():
	global root
	f = open("spodiro_path.txt")
	lines = f.readlines()
	line = lines.pop().strip()
	root = line

get_root()		
read_config(join(root, "resource/spodiro_config.txt"))
read_fst_config("fst_config_gen.txt")
write_jsgfs()
write_fst_config("fst_config_gen.txt")




		
