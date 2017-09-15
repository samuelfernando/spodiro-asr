import socket
import StringIO
import struct
import numpy as np
import time
import datetime
import subprocess
import sys

TCP_IP = '192.168.161.127'
TCP_PORT = 5005
BUFFER_SIZE = 10920  # Normally 1024, but we want fast response
#BUFFER_SIZE = 32768

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connection address:', addr


	
def recv_all(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = ''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

outfile = None;
textfile = None;
aOutfile = [None]*(4-1); # ASSUME max nbr channels = 4

p = subprocess.Popen(["/home/samf/spodiro-asr/pepper.sh"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

while 1:
	
	num_data = recv_all(conn, BUFFER_SIZE+4)#.recv(BUFFER_SIZE)

#	if not num_data: break
	
	sio = StringIO.StringIO(num_data)
	pack_num = sio.read(4)
	unpacked = struct.unpack("i", pack_num)[0]

	#print("received "+str(unpacked))
	
	data = sio.read()
	
	aSoundDataInterlaced = np.fromstring( str(data), dtype=np.int16 );
	aSoundData = np.reshape( aSoundDataInterlaced, (4, 1365), 'F' );
	
	avg = np.mean(aSoundData, axis=0, dtype=np.int16)
	
	#byt = avg.tostring()
	#print(len(byt))
	p.stdin.write(avg.tostring())

	if( outfile == None ):
		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')
		strFilenameOut = st+"_0.raw";
		textfile = open(st+".txt", "w");
		print( "INF: Writing sound to '%s'" % strFilenameOut );
		outfile = open( strFilenameOut, "wb" );
		for nNumChannel in range( 1, 4 ):
			strFilenameOutChan = strFilenameOut.replace("_0.raw", "_%d.raw"%nNumChannel);
			aOutfile[nNumChannel-1] = open( strFilenameOutChan, "wb" );
			print( "INF: Writing other channel sound to '%s'" % strFilenameOutChan );
   
	aSoundData[0].tofile( outfile ); # wrote only one channel
	for nNumChannel in range( 1, 4 ):
		aSoundData[nNumChannel].tofile( aOutfile[nNumChannel-1] ); 

        
 #   print "received data:", data
  #  conn.send(data)  # echo
conn.close()

