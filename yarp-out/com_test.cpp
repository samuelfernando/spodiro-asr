#include <string>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

using namespace std;


int main(int argc, char *argv[]) {
	FILE* pipe = popen(run_file, "r");
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

}

