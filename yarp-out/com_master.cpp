#include <string>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <signal.h>

using namespace std;


int main(int argc, char *argv[]) {

	pid_t pid;
	int rpipes[2];
	int wpipes[2];
	FILE* output;
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
		dup2(rpipes[1], STDERR_FILENO);
		//cout << pipefd[1] << endl;
		char wpipe_num[20];
		char rpipe_num[20];
		sprintf(wpipe_num, "%d", wpipes[0]);
		sprintf(rpipe_num, "%d", rpipes[1]);
		
		execl("./com_slave", wpipe_num, rpipe_num, (char*) NULL);
		
		// Nothing below this line should be executed by child process. If so,
		// it means that the execl function wasn't successfull, so lets exit:
		exit(1);
	}
	// The code below will be executed only by parent. You can write and read
	// from the child using pipefd descriptors, and you can send signals to
	// the process using its pid by kill() function. If the child process will
	// exit unexpectedly, the parent process will obtain SIGCHLD signal that
	// can be handled (e.g. you can respawn the child process).

	// Now, you can write to the process using pipefd[0], and read from pipefd[1]:

	//write(pipefd[0], "message", strlen("message")); // write message to the process
	//write(pipefd[1], "message", strlen("message"));
	write(wpipes[1], "message", strlen("message"));
	
	while (true) {
		int size = read(rpipes[0], buf, sizeof(buf)); // read from the process. Note that this will catch
	// standard  output together with error output
		//if (out==1) {
			//cout << "ret " << out << endl;
			std::string str(buf, size);
			cout << str;
		//}
		//usleep(1000000);
		
	}
	kill(pid, 9);



}

