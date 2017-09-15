#include <string>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

using namespace std;


int main(int argc, char *argv[]) {
	
	
	int read_pipe = atoi(argv[0]); // the other process write
	int write_pipe = atoi(argv[1]); // the other process read
	
	//cout << "slave read " << read_pipe << endl;
	//cout << "slave write " << write_pipe << endl;
	
	//std::string str;
	
	//cin >> str;
	//cout << str << endl;
	char buf[20];
	
	int size = read(read_pipe, buf, sizeof(buf));
	//cout << "slave size = " << size << endl;
	std::string str(buf, size);
	//cout << "slave " << str << endl;
	std::string base = "Hello";
	if (str == "message") {
		base = "Goodbye";
	}
	
	for (int i=0;i<10;++i) {
		cout << "slave " << base << " " << i << endl;
		//char out[20];
		//sprintf(out, "slave Hello %d", i);
		//write(write_pipe, out, strlen(out));
		usleep(2000000);
	}

}

