#include <string>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <yarp/os/all.h>
#include <string.h>

using namespace std;
using namespace yarp::os;


int main(int argc, char *argv[]) {
	Network yarp;
	BufferedPort<Bottle> inPort, outPort;
	//bool ok = inPort.open("/hello/in");
	bool ok = outPort.open("/asr_write");
	ok = ok && inPort.open("/activate_read");
	if (!ok) {
		fprintf(stderr, "Failed to create ports.\n");
		fprintf(stderr, "Maybe you need to start a nameserver (run 'yarpserver')\n");
		return 1;
	}

	//yarp.connect(outPort.getName(),inPort.getName());
	char* run_file = argv[1];

	
	char buffer[256];
	yarp.connect("/asr_write","/asr_read");
	yarp.connect("/activate_write","/activate_read");
	
	Bottle *in;
	
	in = inPort.read();
    
    cout << "message received" << endl;
    
    cout << in->toString() << endl;
   /* FILE* pipe = popen(run_file, "r");
	if (!pipe) {
		printf("ERROR");
		::exit(0);
	}
    
	while(!feof(pipe)) {

		if(fgets(buffer, 256, pipe) != NULL) {
			Bottle&out = outPort.prepare();
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
*/
}

