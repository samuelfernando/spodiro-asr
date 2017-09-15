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
int rpipes[2];
int wpipes[2];
Network myYarp;
BufferedPort<Bottle> inPort;
BufferedPort<Bottle> overridePort;
BufferedPort<Bottle> lmPort;
BufferedPort<Bottle> outPort;
BufferedPort<Bottle> controlPort;
bool my_terminate = false;
//bool shouldRecognise = false;
bool writeLock = false;

void my_log(string s) {
	
	timeval curTime;
	gettimeofday(&curTime, NULL);
	int milli = curTime.tv_usec/1000;
	char buffer[80];
	strftime(buffer, 80, "%d-%m-%Y-%H:%M:%S", localtime(&curTime.tv_sec));
	char currentTime[84]="";
	
	sprintf(currentTime, "%s:%03d", buffer, milli);
	s.erase(s.find_last_not_of(" \n")+1);
	while (writeLock) {}
	writeLock = true;
	cerr << currentTime << " " << s << endl;
	writeLock = false;
}

void start_termination() {
	my_terminate = true;
	Bottle&out = controlPort.prepare();
	out.clear();
	out.addString("terminate");
	controlPort.write(true);
	string send = "terminate\n";
	const char* c_str = send.c_str();
	write(wpipes[1], c_str, strlen(c_str));
}

void open_port(BufferedPort<Bottle> *port, const char* port_name) {
	bool ok = port->open(port_name);
	if (!ok) {
		fprintf(stderr, "Failed to create ports.\n");
		fprintf(stderr, "Maybe you need to start a nameserver (run 'yarpserver')\n");
	}
}

void* start_reader(void* This) {
	//cerr << "Starting reader" << endl;
	my_log("Starting reader");
	char buf[255];
	open_port(&outPort, "/SpeechRecognition/Sentence:o");
	myYarp.connect("/SpeechRecognition/Sentence:o", "/DialogueController/Speech:i");

	while (!my_terminate) {
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
			out.addString("input");
			out.addString(str);
			//printf("Sending %s\n", out.toString().c_str());
			//cerr << str << endl;
			//my_log(str);
			outPort.write(true);
		}
	}
	cout << "reader terminated!" << endl;
}
void* start_lm(void* This) {
	//cerr << "Starting lm" << endl;
	my_log("Starting lm");
	open_port(&lmPort, "/SpeechRecognition/LMChange:i");
	myYarp.connect("/QuizController/DialogueUtt:o", "/SpeechRecognition/LMChange:i");
	char *send = new char[255];
	while (!my_terminate) {
		Bottle *bot = lmPort.read();
		//cerr << "About to read bottle" << endl;
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
			if (i!=-999) {
				ostringstream ss;
				ss.clear();
				ss << "lm_change " << str_type << " " << i << "\n";
				string lm_send = ss.str();
				//my_log("Sending on YARP message "+lm_send);
			
				//cerr << "ASR_master sending " << lm_send << endl;
				//my_log(lm_send);
				const char* c_str = lm_send.c_str();
				write(wpipes[1], c_str, strlen(c_str));
			}
		}

	}
	my_log("lm terminated");
	//cout << "lm terminated!" << endl;
}
void* start_controller(void* This) {
	//cerr << "Starting controller" << endl;
	my_log("Starting controller");
	open_port(&inPort, "/SpeechRecognition/Control:i");
	myYarp.connect("/DialogueController/DialogueSpeechFeedback:o", "/SpeechRecognition/Control:i");
	myYarp.connect("/DialogueController/SpeechFeedback:o", "/SpeechRecognition/Control:i");
	myYarp.connect("/ASRGui/ButtonControl:o", "/SpeechRecognition/Control:i");

	char *send = new char[255];

	while (!my_terminate) {
		Bottle *bot = inPort.read();
		std::string str = bot->get(0).asString();
		
		if (str=="speech_event") {
			std::string str = "speech_event "+bot->get(1).asString() +"\n";
			//cerr << "Received " << str << endl;
			const char* c_str = str.c_str();
			//my_log("Sending on YARP message "+str);
			write(wpipes[1], c_str, strlen(c_str));
		}
		else if (str=="button_control") {
			std::string str = "button_control "+bot->get(1).asString() +"\n";
			//cerr << "Received '" << str << "'" << endl;
			const char* c_str = str.c_str();
			//my_log("Sending on YARP message "+str);
			write(wpipes[1], c_str, strlen(c_str));
			
		}
	}
	my_log("controller terminated");
	//cout << "controller terminated!" << endl;
}

void* start_override(void* This) {
	//cerr << "Starting override" << endl;
	my_log("Starting override thread");
	open_port(&overridePort, "/SpeechRecognition/Override:i");
	myYarp.connect("/DialogueController/SpeechOverride:o", "/SpeechRecognition/Override:i");
	
	char *send = new char[255];

	while (!my_terminate) {
		Bottle *bot = overridePort.read();
		std::string str = bot->get(0).asString();
		//my_log("Sending on YARP message "+str);
		if (str=="speech_override") {
			std::string str = "speech_override "+bot->get(1).asString() +"\n";
			//cerr << "Received " << str << endl;
			//my_log("Sending on YARP message "+str);
			const char* c_str = str.c_str();
			write(wpipes[1], c_str, strlen(c_str));
		}
	}
	my_log("Overrride thread terminated");
	//cout << "override terminated!" << endl;
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
		//cout << "Read pipe should be " << wpipe_num << endl;
		const char* prog = "./new_recogniser.sh";
		
		execl(prog, prog, wpipe_num, (char*) NULL);

		// Nothing below this line should be executed by child process. If so,
		// it means that the execl function wasn't successfull, so lets exit:
		//cout << "FATAL ERROR shouldn't get here " << endl;
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


/*
void check_for_keypress() {

	struct termios oldSettings, newSettings;
	tcgetattr( fileno( stdin ), &oldSettings );
	newSettings = oldSettings;
	newSettings.c_lflag &= (~ICANON & ~ECHO);
	tcsetattr( fileno( stdin ), TCSANOW, &newSettings );

	while ( !my_terminate )
	{
		fd_set set;
		struct timeval tv;

        tv.tv_sec = 0;
        tv.tv_usec = 100000;
        
		FD_ZERO( &set );
		FD_SET( fileno( stdin ), &set );
		int res = select( fileno( stdin )+1, &set, NULL, NULL, &tv );
		if( res > 0 )
		{
			char c;
			read( fileno( stdin ), &c, 1 );
			my_log("Received keypress" + c);
			if (c=='T') {
				start_termination();
			}
		}
		else if( res < 0 )
		{
			perror( "select error" );
			break;
		}
		else
		{
			//printf( "Select timeout\n" );
		}
	}
	tcsetattr( fileno( stdin ), TCSANOW, &oldSettings );
}*/
int main(int argc, char *argv[]) {

	open_port(&controlPort, "/SpeechRecognition/MasterControl:o");
	int pid = fork_recogniser();
	
	//cout << "PID " << pid << endl;
	pthread_t* lm_thread = new pthread_t();
	pthread_t* controller_thread = new pthread_t();
	pthread_t* reader_thread = new pthread_t();
	pthread_t* override_thread = new pthread_t();
	
	start_thread(controller_thread, start_controller);
	start_thread(reader_thread, start_reader);
	start_thread(override_thread, start_override);
	start_thread(lm_thread, start_lm);
	
	myYarp.connect("/SpeechRecognition/MasterControl:o", "/SpeechRecognition/Control:i");
	myYarp.connect("/SpeechRecognition/MasterControl:o", "/SpeechRecognition/LMChange:i");
	//check_for_keypress();
	pthread_join( *controller_thread, NULL);
	pthread_join( *reader_thread, NULL);
	pthread_join( *lm_thread, NULL);
	pthread_join( *override_thread, NULL);
	
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
	
	controlPort.close();
	inPort.close();
	outPort.close();
	lmPort.close();
	return 0;
	

}
