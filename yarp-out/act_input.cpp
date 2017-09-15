#include <string>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <yarp/os/all.h>
#include <string.h>
#include <unistd.h>

using namespace std;
using namespace yarp::os;


int main(int argc, char *argv[]) {
	Network yarp;
	BufferedPort<Bottle> inPort, outPort;
	//bool ok = inPort.open("/hello/in");
	bool ok = outPort.open("/asr_write");
	ok = ok && inPort.open("/zeno_read");
	if (!ok) {
		fprintf(stderr, "Failed to create ports.\n");
		fprintf(stderr, "Maybe you need to start a nameserver (run 'yarpserver')\n");
		return 1;
	}

	//yarp.connect(outPort.getName(),inPort.getName());
	

	
	
	yarp.connect("/asr_write","/asr_read");
	yarp.connect("/zeno_write","/zeno_read");
	
	Bottle *in;
	
	cout << "Waiting to receive "  << endl;
	in = inPort.read();
    
    cout << "Received " << in->toString() << endl;
    
    //usleep(1*1000*1000);
    char* run_file = argv[1];
    char buffer[256];
    FILE* pipe = popen(run_file, "r");
	if (!pipe) {
		printf("ERROR");
		::exit(0);
	}
	
	Bottle& out = outPort.prepare();
	out.clear();
	string trigger_str("asr_ready");
	out.addString(trigger_str);
	printf("Sending %s\n", out.toString().c_str());
	outPort.write(true);
    
	while(!feof(pipe)) {

		if(fgets(buffer, 256, pipe) != NULL) {
			out = outPort.prepare();
			out.clear();
			std::string str(buffer);
			str.erase(str.find_last_not_of(" \n")+1);		
			if (str.length()>0) {
				out.addString(str);
				printf("Sending %s\n", out.toString().c_str());
				outPort.write(true);
			}
		}



	}
	
	pclose(pipe);

}

