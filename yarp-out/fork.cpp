#include <string>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

using namespace std;


int main(int argc, char *argv[]) {
	int read_pipe = atoi(argv[0]);
	bool my_terminate = false;
	while (!my_terminate) {
		char buf[255];
		cout << "active" << endl;
		int size = read(read_pipe, buf, sizeof(buf));
		std::string str(buf, size-1);
		cout << "Received '" << str << "'" << endl;
		if (str=="terminate") {
			my_terminate = true;
		}
		
		usleep(100000);
	}

}

