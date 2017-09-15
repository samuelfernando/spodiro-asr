import sys
from subprocess import PIPE, Popen
from threading  import Thread
import time

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x

ON_POSIX = 'posix' in sys.builtin_module_names

class Process:
	def __init__(self, process_name):
		self.p = Popen([process_name], stdout=PIPE, stdin=PIPE)#, bufsize=1, close_fds=ON_POSIX)
		self.q = Queue()
		self.t = Thread(target=self.enqueue_output, args=(self.p.stdout, self.q))
		self.t.daemon = True # thread dies with the program

	def enqueue_output(self, out, queue):
		for line in iter(out.readline, b''):
			queue.put(line)
		out.close()
	
	def start(self):
		self.t.start()
		self.active = True
		
	def listen(self, output):
# read line without blocking
		try:  line = self.q.get_nowait() # or q.get(timeout=.1)
		except Empty:
			return None
		else: # g	
			out = line.strip()
			if output:
				print(out)
			return line.strip()
		time.sleep(0.01)

	def loop_listen_aux(self):
		while self.active:
			self.listen(True)
		
	def loop_listen(self):
		self.l = Thread(target=self.loop_listen_aux)
		self.l.daemon = True
		self.l.start()

			
	def stop(self):
		self.p.terminate()
		self.active = False
		self.l.join()
		self.t.join()

	def write(self, s):
		self.p.stdin.write(s)
