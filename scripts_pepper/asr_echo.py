import qi
import time
import sys
import argparse
import numpy as np
import struct
from naoqi import ALProxy
from process import Process
import socket
import StringIO

TCP_IP = '192.168.161.127'
TCP_PORT = 5005
BUFFER_SIZE = 10920  

class HumanGreeter(object):
    """
    A simple class to react to face detection events.
    """

    def __init__(self, app):
        """
        Initialisation of qi framework and event detection.
        """
        super(HumanGreeter, self).__init__()
        app.start()
        session = app.session
        # Get the service ALMemory.
        self.memory = session.service("ALMemory")
        # Connect the event callback.
        #self.subscriber = self.memory.subscriber("FaceDetected")
       # self.subscriber.signal.connect(self.on_human_tracked)
        # Get the services ALTextToSpeech and ALFaceDetection.
        self.p = Process("/home/samf/spodiro-asr/pepper.sh", self.respond)
        self.tts = ALProxy("ALTextToSpeech", "192.168.161.126", 9559)
       	self.start_speech = self.memory.subscriber("ALTextToSpeech/TextStarted")
       	self.end_speech = self.memory.subscriber("ALTextToSpeech/TextDone")      
        self.start_speech.signal.connect(self.speech_started)
        self.end_speech.signal.connect(self.speech_ended)
        self.p.start()
        self.p.loop_listen()
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)
        self.conn, addr = s.accept()
        print 'Connection address:', addr
        self.should_listen = True
        #self.face_detection = session.service("ALFaceDetection")
        #self.face_detection.subscribe("HumanGreeter")
        #self.got_face = False

    def respond(self, text):
        self.tts.say(text)
	
    def recv_all(self, sock, n):
        data = ''
        while len(data) < n:
    		packet = sock.recv(n - len(data))
    		if not packet:
    			return None
    		data += packet
    	return data
    	
    def speech_started(self, value):
    	if value:
    		self.should_listen = False
    		print("speech started")
    
    def speech_ended(self, value):
    	if value:
    		self.should_listen = True
    		print("speech ended")

    def run(self):
        """
        Loop on, wait for events until manual interruption.
        """
        print "Starting HumanGreeter"
        try:
            while True:
            	num_data = self.recv_all(self.conn, BUFFER_SIZE+4)#.recv(BUFFER_SIZE)
                sio = StringIO.StringIO(num_data)
                pack_num = sio.read(4)
                unpacked = struct.unpack("i", pack_num)[0]
                data = sio.read()
                aSoundDataInterlaced = np.fromstring( str(data), dtype=np.int16 );
                aSoundData = np.reshape( aSoundDataInterlaced, (4, 1365), 'F' );
	
                avg = np.mean(aSoundData, axis=0, dtype=np.int16)
                if self.should_listen:
                	self.p.write(avg.tostring())
        except KeyboardInterrupt:
            self.conn.close()
            print "Interrupted by user, stopping HumanGreeter"
           
            sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["HumanGreeter", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    human_greeter = HumanGreeter(app)
    human_greeter.run()