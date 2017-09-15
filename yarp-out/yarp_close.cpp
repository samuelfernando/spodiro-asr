#include <string>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <yarp/os/all.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>
#include <iterator>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <termios.h>


using namespace std;
using namespace yarp::os;

Network myYarp;
BufferedPort<Bottle> inPort;
BufferedPort<Bottle> extPort;

 bool my_terminate = false;
 
 int rpipes[2];
int wpipes[2];

void* start_reader(void* This) {
	
	cerr << "Starting reader" << endl;
	char buf[255];

	while (true) {
		int size = read(rpipes[0], buf, sizeof(buf));
		std::string str(buf, size-1);
		cerr << "Received " << str << endl;
	}
}

void* start_controller(void* This) {
	cerr << "Starting controller" << endl;
	bool ok = inPort.open("/Test/Read:i");
	ok = extPort.open("/External/Write:o");
	
	if (!ok) {
		fprintf(stderr, "Failed to create ports.\n");
		fprintf(stderr, "Maybe you need to start a nameserver (run 'yarpserver')\n");
	}
	
	myYarp.connect("/External/Write:o", "/Test/Read:i");
	
	while (!my_terminate) {
		cerr << "waiting for read" << endl;
		Bottle *bot = inPort.read();
		cerr << "read completed" << endl;

		std::string str = bot->get(0).asString();
		cerr << "Received " << str << endl;
	}
	inPort.close();
	extPort.close();
}

int fork_recogniser() {
	
	pid_t pid;
	char buf[10];

	pipe(rpipes);
	pipe(wpipes);
	pid = fork();
	
	if (pid == 0)
	{
		// Child
		close(wpipes[1]);
		close(rpipes[0]);
		dup2(wpipes[0], STDIN_FILENO);
		dup2(rpipes[1], STDOUT_FILENO);

		//dup2(rpipes[1], STDERR_FILENO);
		//cout << pipefd[1] << endl;
		char wpipe_num[20];
		char rpipe_num[20];
		sprintf(wpipe_num, "%d", wpipes[0]);
		sprintf(rpipe_num, "%d", rpipes[1]);

		execl("./fork", wpipe_num, (char*) NULL);
		
		

		// Nothing below this line should be executed by child process. If so,
		// it means that the execl function wasn't successfull, so lets exit:
		cout << "FATAL ERROR shouldn't get here " << endl;
	}
	return pid;

}

void start_thread(pthread_t* thread, void *(*function) (void *)) {


	int iret;
	iret = pthread_create( thread, NULL, function, NULL);
	if(iret)
	{

		fprintf(stderr,"Error - pthread_create() return code: %d\n",iret);

	}
	
	
	
}

void check_for_keypress() {
	struct termios oldSettings, newSettings;

    tcgetattr( fileno( stdin ), &oldSettings );
    newSettings = oldSettings;
    newSettings.c_lflag &= (~ICANON & ~ECHO);
    tcsetattr( fileno( stdin ), TCSANOW, &newSettings );    

   
    while ( !my_terminate )
    {
        fd_set set;

        FD_ZERO( &set );
        FD_SET( fileno( stdin ), &set );

        int res = select( fileno( stdin )+1, &set, NULL, NULL, NULL );

        if( res > 0 )
        {
            char c;
            read( fileno( stdin ), &c, 1 );
            cerr << "Received " << c << endl;
            if (c=='T') {
            	my_terminate = true;
            	Bottle&out = extPort.prepare();
            	out.clear();
            	out.addString("terminate");
            	extPort.write(true);
            	string send = "terminate\n";
            	const char* c_str = send.c_str();
			  	write(wpipes[1], c_str, strlen(c_str));
            }
        }
        else if( res < 0 )
        {
            perror( "select error" );
            break;
        }
        else
        {
            printf( "Select timeout\n" );
        }
    }

    tcsetattr( fileno( stdin ), TCSANOW, &oldSettings );
}


int main(int argc, char *argv[]) {
	
	
	
	int pid = fork_recogniser();
	
	pthread_t* controller_thread  = new pthread_t();
	pthread_t* reader_thread = new pthread_t();
	start_thread(controller_thread, start_controller);
	start_thread(reader_thread, start_reader);
	
	check_for_keypress();
	
	
    pthread_join( *controller_thread, NULL);
    int returnStatus;    
    waitpid(pid, &returnStatus, 0);  // Parent process waits here for child to terminate.

    if (returnStatus == 0)  // Verify child process terminated without error.  
    {
       std::cout << "The child process terminated normally." << std::endl;    
    }

    if (returnStatus == 1)      
    {
       std::cout << "The child process terminated with an error!." << std::endl;    
    }
    
    return 0;
}

