#include <string>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <yarp/os/all.h>
#include <string.h>

using namespace std;
using namespace yarp::os;


int main(int argc, char *argv[]) {
	
	char* run_file = argv[1];
	char* port_name= argv[2];
	
	Network yarp;
	BufferedPort<Bottle> inPort,outPort;
	string out_name(port_name);
	string in_name(port_name);
	
	out_name=out_name+":o";
	in_name=in_name+":i";
	
	bool ok = inPort.open(in_name);
	ok = ok && outPort.open(out_name);
	if (!ok) {
		fprintf(stderr, "Failed to create ports.\n");
		fprintf(stderr, "Maybe you need to start a nameserver (run 'yarpserver')\n");
		return 1;
	}

	//yarp.connect(outPort.getName(),inPort.getName());
	

	FILE* pipe = popen(run_file, "r");
	if (!pipe) {
		printf("ERROR");
		::exit(0);
	}
	char buffer[256];
	yarp.connect(out_name,in_name);
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

}

