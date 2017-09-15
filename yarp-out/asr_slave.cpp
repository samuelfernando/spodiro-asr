#include <string>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

using namespace std;

int read_pipe = -1;

void* start_receiver(void* This) {

	while (true) {
		char buf[255];
	
		int size = read(read_pipe, buf, sizeof(buf));
		//cout << "size = " << size << endl;
		std::string str(buf, size);
		//cout << "Received " << str << endl;
		//cout << str << endl;
		usleep(1000);
		//usleep(100000);
	}
}

int main(int argc, char *argv[]) {
	
	
	read_pipe = atoi(argv[0]); // the other process write
	//cout << read_pipe << endl;
	pthread_t receiver_thread;

	
	int iret = pthread_create( &receiver_thread, NULL, start_receiver, NULL);
	if(iret)
	{

		fprintf(stderr,"Error - pthread_create() return code: %d\n",iret);

	}
	pthread_join( receiver_thread, NULL);


}

