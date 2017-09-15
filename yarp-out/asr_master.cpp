#include <string>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <yarp/os/all.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>
#include <iterator>


using namespace std;
using namespace yarp::os;

int rpipes[2];
int wpipes[2];

Network myYarp;
BufferedPort<Bottle> inPort;
BufferedPort<Bottle> lmPort;
BufferedPort<Bottle> outPort;
pthread_t* controller_thread;
pthread_t* reader_thread;
pthread_t* lm_thread;
//bool shouldRecognise = false;

void* start_reader(void* This) {
	
		cerr << "Starting reader" << endl;
	char buf[255];
	bool ok = outPort.open("/SpeechRecognition/Sentence:o");
	
	if (!ok) {
		fprintf(stderr, "Failed to create ports.\n");
		fprintf(stderr, "Maybe you need to start a nameserver (run 'yarpserver')\n");
	}
	
	myYarp.connect("/SpeechRecognition/Sentence:o", "/DialogueController/Speech:i");


	while (true) {
		//cout << "Starting reader read" << endl;
		int size = read(rpipes[0], buf, sizeof(buf));
		//cout << "size = " << size << endl;
		//std::string str(buf, size);
		
		std::string str(buf, size-1);
		//cout << str << endl;
		Bottle&out = outPort.prepare();
		out.clear();
		//out.addString(str);
		//outPort.write(true);
		
		str.erase(str.find_last_not_of(" \n")+1);		
			if (str.length()>0) {
				out.addString(str);
				//printf("Sending %s\n", out.toString().c_str());
				cerr << str << endl;
				outPort.write(true);
			}
		
	}
}

void* start_lm(void* This) {
	cerr << "Starting lm" << endl;
	bool ok = lmPort.open("/SpeechRecognition/LMChange:i");
	if (!ok) {
		fprintf(stderr, "Failed to create ports.\n");
		fprintf(stderr, "Maybe you need to start a nameserver (run 'yarpserver')\n");
	}
	
	myYarp.connect("/QuizController/DialogueUtt:o", "/SpeechRecognition/LMChange:i");
	
	char *send = new char[255];

	// Send initial information to the controller
	// The arguments received from the shell script in order
	
	/*for (int i=0;i<globargc;++i) {
		sprintf(send, "%s", globargv[i]);
		
		//sprintf(send, "%d %s", i, globargv[i]);
		
		write(wpipes[1], send, strlen(send));	
		usleep(1000);
	}
	send = (char*)"ENDOFARGUMENTLIST";
	write(wpipes[1], send, strlen(send));	
	*/			
	
	// Read from the input YARP port and pass it on to the interactive decoder
	//cerr << "Starting YARP reader thread" << endl;
	while (true) {
		Bottle *bot = lmPort.read();
		cerr << "About to read bottle" << endl;
		std::string str = bot->get(0).asString();
		if (str=="status" && bot->size()>1) {
			
		
			Value stat_list = bot->get(1);
			Bottle *list = stat_list.asList();
			Value type = list->get(0);
			string str_type = type.asString();
			//cerr << "Dialogue type " << str_type << endl;

			Value num = list->get(1);
			int i = num.asInt();
			//cerr << "Utt no " << i << endl; 
			ostringstream ss;
			ss.clear();
			
			ss << "lm_change " << str_type << " " << i << "\n";
			string lm_send = ss.str();
			
			cerr << "ASR_master sending " << lm_send << endl;
				const char* c_str = lm_send.c_str();
			  	write(wpipes[1], c_str, strlen(c_str));
		}
		
	
		/*for (int i=0;i<bot->size();++i) {
			
			if (str=="status") 
			cerr << "Received " << str << endl;
			const char* c_str = str.c_str();
			write(wpipes[1], c_str, strlen(c_str));

		}*/
	}
}
void* start_controller(void* This) {
		cerr << "Starting controller" << endl;
		  	cerr << "write pipe" << wpipes[1] << endl;
			
	bool ok = inPort.open("/SpeechRecognition/Control:i");
	if (!ok) {
		fprintf(stderr, "Failed to create ports.\n");
		fprintf(stderr, "Maybe you need to start a nameserver (run 'yarpserver')\n");
	}
	
	myYarp.connect("/DialogueController/SpeechFeedback:o", "/SpeechRecognition/Control:i");
	
	
	char *send = new char[255];

	// Send initial information to the controller
	// The arguments received from the shell script in order
	
	/*for (int i=0;i<globargc;++i) {
		sprintf(send, "%s", globargv[i]);
		
		//sprintf(send, "%d %s", i, globargv[i]);
		
		write(wpipes[1], send, strlen(send));	
		usleep(1000);
	}
	send = (char*)"ENDOFARGUMENTLIST";
	write(wpipes[1], send, strlen(send));	
	*/			
	
	// Read from the input YARP port and pass it on to the interactive decoder
	//cerr << "Starting YARP reader thread" << endl;
	while (true) {
		Bottle *bot = inPort.read();
		std::string str = bot->get(0).asString();
	
		
		if (str=="speech_event") {
			
			  	std::string str = "speech_event "+bot->get(1).asString() +"\n";
			  	//cerr << "Received " << str << endl;
			  	const char* c_str = str.c_str();
			  	
			  	write(wpipes[1], c_str, strlen(c_str));
			
		}
		/*for (int i=0;i<bot->size();++i) {
			
			if (str=="status") 
			cerr << "Received " << str << endl;
			const char* c_str = str.c_str();
			write(wpipes[1], c_str, strlen(c_str));

		}*/
	}
}


int main(int argc, char *argv[]) {
	//Network::setLocalMode(true);
	//char* run_file = argv[1];
	
	
	//std::copy(std::begin(argv), std::end(argv), std::begin(globargv));
	//globargv = argv;
	//globargc = argc;
	//globargv = new char*[argc];
	
		//cout <<  i << " " << globargv[i] << endl;
	
	/*	bool ok = outPort.open(port_name);
		if (!ok) {
			fprintf(stderr, "Failed to create ports.\n");
			fprintf(stderr, "Maybe you need to start a nameserver (run 'yarpserver')\n");
			return 1;
		}*/

		
	// we are going to fork off a new process that will be controlling the ASR
	// we write the pipe ids to global variables so that the other thread can access them
	
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

		cout << "read_pipe should be " << wpipe_num << endl;
		const char* prog = "./new_recogniser.sh";
		
		execl(prog, prog, wpipe_num, (char*) 0);
		
		

		// Nothing below this line should be executed by child process. If so,
		// it means that the execl function wasn't successfull, so lets exit:
		cout << "FATAL ERROR shouldn't get here " << endl;
	}
	

	int  iret;
	lm_thread = new pthread_t();
	controller_thread = new pthread_t();
	reader_thread = new pthread_t();
	iret = pthread_create( controller_thread, NULL, start_controller, NULL);
	if(iret)
	{

		fprintf(stderr,"Error - pthread_create() return code: %d\n",iret);

	}
	


	
	
	iret = pthread_create( reader_thread, NULL, start_reader, NULL);
	if(iret)
	{

		fprintf(stderr,"Error - pthread_create() return code: %d\n",iret);

	}
	
		iret = pthread_create( lm_thread, NULL, start_lm, NULL);
	if(iret)
	{

		fprintf(stderr,"Error - pthread_create() return code: %d\n",iret);

	}


	pthread_join( *controller_thread, NULL);

	pthread_join( *reader_thread, NULL);
	
	pthread_join( *lm_thread, NULL);


	//start ASR slave (i.e. reader.sh)


	//start InputThread .. runs continuously waiting for input





	//yarp.connect(outPort.getName(),inPort.getName());



}

