from subprocess import call
from os import listdir
from os.path import isfile, join, splitext
import re

target = "fixed"
src = "broken"



onlyfiles = [ f for f in listdir(src) if isfile(join(src,f)) and splitext(f)[1]==".wav" ]
for filename in onlyfiles:
	old = join(src, filename)
	new = join(target, filename)
	print(old, new)
	call(["sox", "--ignore-length", old, new])


