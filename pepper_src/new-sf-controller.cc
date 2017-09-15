#include "my-online.h"
#include <signal.h>

// receives some data from the data source, and decodes it
namespace kaldi {

SFController* SFController::instance;

void SFController::my_log(string s) {
	char currentTime[84];
	get_timestamp(currentTime);
	while (writeLock) {}
	
	writeLock = true;
	cerr << currentTime << " " << s << endl;
	writeLock = false;
}

void SFController::get_timestamp(char* currentTime) {
	timeval curTime;
	gettimeofday(&curTime, NULL);
	int milli = curTime.tv_usec/1000;
	char buffer[80];
	strftime(buffer, 80, "%d-%m-%Y-%H:%M:%S", localtime(&curTime.tv_sec));
	//char currentTime[84]="";
	sprintf(currentTime, "%s:%03d", buffer, milli);
	//return currentTime;
}

SFController::SFController(int argc, char* argv[]) {
	this -> argc = argc;
	this -> argv = argv;
	this -> writeLock = false;
	for (int i=0;i<argc;++i) {
		//cerr << argv[i] << endl;
	}
	this -> startListening = argv[argc-2];

	//this->read_pipe = atoi(argv[argc-3]);
	this->read_pipe = STDIN_FILENO;
	//cerr << "read pipe " << read_pipe << endl;
	string write = "read pipe ";
	write.append(argv[argc-3]);
	my_log(write);
	active = false;
	//my_buffer = new BaseFloat[8000];
	this -> should_listen = true;
	this -> always_listen = false;
	this -> sample_count = 0;
	controller_thread = new pthread_t();
	this -> prevData = new RingBuffer(14);
	
	
	
	/*	cerr << "decode_type " << decode_type << endl;
		cerr << "should_listen " << should_listen << endl;
		cerr << "read_pipe " << read_pipe << endl;
		cerr << "record_wav " << record_wav << endl;
		cerr << "keyphrase " << keyphrase << endl;
		cerr << "output_path " << output_path << endl;
		cerr << "source "<< source << endl;
		cerr << "utt " << utt << endl;
		cerr << "interactive " << interactive << endl;*/

}

void SFController::hear(Vector<BaseFloat>* data) {
	
	using namespace std;
	if (should_listen) {
		decoder -> hear(data);
	}
	
}

void SFController::refresh_date() {
	time_t t = time(0);   // get time now
	struct tm * now = localtime( & t );
	char buffer[80];
	strftime(buffer,80,"%d_%m_%Y_%H_%M_%S",now);
	date_string = new string(buffer);
	char daybuf[80];
	strftime(daybuf,80,"%d_%m_%Y", now);
	day_string = new string(daybuf);
}

void SFController::input_finished() {
	//cout << "input finished"<<endl;
	decoder->input_finished_func();
	decoder->stop();
	//listener -> input_finished_func();
	//listener -> stop();
}

void SFController::add_chunk(int size) {
	//cout << "adding chunk" << endl;
	output->add_chunk(size);
}

std::string SFController::get_date_string() {
	return *date_string;
}

std::string SFController::get_day_string() {
	return *day_string;
}

void SFController::startDecoder() {
	//cout << "SFController startDecoder" << endl;
	//cout << "type" << gen_config->decode_type << endl;
	if (!strcmp(gen_config->decode_type, "nnet")) {
		//cout << "About to open the SFNnetDecoder" << endl;
//		decoder = new SFNnetDecoder(this, (SFNnetConfig*)decode_config, gen_config->keyphrase);
		decoder = new SFNnetThreadedDecoder(this, (SFNnetThreadedConfig*)decode_config, gen_config->keyphrase);
	
	}
	else if (!strcmp(gen_config->decode_type, "gmm")) {
		decoder = new SFGmmDecoder(this, (SFGmmConfig*)decode_config, gen_config->keyphrase);
		//cout << "GMM not implemented yet" << endl;
	}
	else {
		//cout << "Wrong decoder type, must be nnet or gmm" << endl;
	}
	/*if (!strcmp(startListening, "true")) {
		decoder->initListen(true);
}
	else {
		decoder->initListen(false);
}*/


	decoder->start();
}


void SFController::startSource() {
	//cout << "Starting source" << endl;
	if (!strcmp(gen_config->source, "wav")) {
		//cout << "Starting WAV source " << endl;
		src = new WavDataSource(gen_config->utt, this);
	}
	else if (!strcmp(gen_config->source, "pa")) {
		src = new PortAudioDataSource(this, gen_config->output_path, gen_config->record_wav);
	}
	else {
		my_log("WRONG DATA SOURCE, must be PA or WAV");
		//cerr << "WRONG DATA SOURCE, must be PA or WAV" << endl;
	}
	src -> start();
}


std::vector<std::string>& SFController::split(const std::string &s, char delim, std::vector<std::string> &elems) {
	std::stringstream ss(s);
	std::string item;
	while (std::getline(ss, item, delim)) {
		elems.push_back(item);
	}
	return elems;
}

void SFController::waitForFinish() {
	
	pthread_join( *controller_thread, NULL);
	close(read_pipe);
}

std::vector<std::string> SFController::split(const std::string &s, char delim) {
	std::vector<std::string> elems;
	split(s, delim, elems);
	return elems;
}

bool SFController::startswith(string prefix, string str) {
	return str.substr(0, prefix.size()) == prefix;
}


void SFController::waitForDecoderFinish() {
	decoder -> waitForFinish();
}

void SFController::waitForSourceFinish() {
	src -> waitForFinish();
}
void SFController::readConfig() {

	//for (int i=0;i<argc;++i) {
	//cout << argv[i] << endl;
	//}

	gen_config = new SFGenericConfig(argc, argv);

	if (!strcmp(gen_config->decode_type, "nnet")) {
		//cerr << "Loading NNET config " << NUM_EXTRA_ARGS << endl;
		my_log("Loading NNET config " + NUM_EXTRA_ARGS);
		//decode_config = new SFNnetConfig(argc - NUM_EXTRA_ARGS, argv);
		decode_config = new SFNnetThreadedConfig(argc - NUM_EXTRA_ARGS, argv);
	
	}
	else {
		
		my_log("Loading GMM config " + NUM_EXTRA_ARGS); 
	//	cerr << "Loading GMM config " << NUM_EXTRA_ARGS << endl;
		decode_config = new SFGmmConfig(argc - NUM_EXTRA_ARGS, argv);

	}

}

void* SFController::startStatic(void* arg) {
	((SFController*)arg)->start_impl();
	return NULL;
}

void SFController::start() {

	int iret = pthread_create( controller_thread, NULL, SFController::startStatic, this);
	if(iret)
	{
		fprintf(stderr,"Error - pthread_create() return code: %d\n",iret);
		exit(EXIT_FAILURE);
	}
	//cout << "start" << endl;
}

int diff_ms(timeval t1, timeval t2)
{
    return (((t1.tv_sec - t2.tv_sec) * 1000000) + 
            (t1.tv_usec - t2.tv_usec))/1000;
}

void SFController::start_impl() {
	refresh_date();
	openOutput();
	startDecoder();
	
//	cerr << "Making date string" << endl;
	string date = get_date_string();
	//cerr << "Making speech out string" << endl;

	string out_str = "speech-out";
	//cerr << "Making day string" << endl;

	string day = get_day_string();
	//cerr << "Making final string" << endl;
	
	//string raw = out_str+"/"+day+"/text/"+date+".wavtext";
	//out_file.open(raw.c_str(),  std::fstream::out);

	string str = out_str+"/"+day+"/speech/"+date+".wav";
	WAV_Writer writer;
	int kSampleFreq = 16000;
	//cerr << "Creating string " << str << " " << str.c_str() << endl;
	Audio_WAV_OpenWriter(&writer, str.c_str(), kSampleFreq, 1);
	active = true;
	//bool first = true;
	int size=1365;
	//char cbuf[100];
	//read(read_pipe, cbuf, sizeof(cbuf)); 
	//cerr << cbuf << " received" << endl;
	int count = 1;
	while (active) { 
		
		int16 buf[size];
		Vector<BaseFloat> kaldi_data(size);
		
		//cerr << "Waiting to read from YARP" << endl;
		int actual_size = read(read_pipe, buf, sizeof(buf));
		//cerr << "received " << count << endl;
		Audio_WAV_WriteShorts( &writer, buf, size);
		//cerr << "Received " << actual_size << endl;
	
		for (int i=0;i<size;++i) {
			kaldi_data.Data()[i] = buf[i];
			
		}
		
		//cerr << "received " << count << " " << avgK << " " << avgB << endl;
	
		hear(&kaldi_data);
		//decoder -> sendMessage(str);
		//usleep(1000);
		//usleep(100000);
		++count;
	}
//	cerr << "Terminated, closing WAV" << endl;
	Audio_WAV_CloseWriter(&writer);
	decoder->stop();
	

}



void SFController::destroy() {
	//cout << "Doing destroy "<<endl;
	decode_config -> destroy();
}

void SFController::openOutput() {
	//cout << "out path " << gen_config -> output_path << endl;

	//cout << "base name " << gen_config -> base_name << endl;
	output = new SFOutput(this, gen_config->source, gen_config->base_name, gen_config->output_path);
}

string SFController::output_string(fst::SymbolTable *word_syms, CompactLattice clat, int64* num_frames, double* tot_like) {
	//cout << " orig output " << endl;
	return output -> output_string(word_syms, clat, num_frames, tot_like, sample_count);
}

void SFController::handle(int s) {

	//cerr << "Handle, passing to terminate" << endl;
	SFController::instance -> terminate();
	//printf("Caught signal %d\n",s);
	//exit(1);
}

void SFController::terminate() {
	//cerr << "Setting active to false" << endl;
	active = false;
	//usleep(10000);
	//src -> stop();
	//if (asrEnabled) {
	//	decoder -> stop();
	//}
	//my_log("Terminated successfully");
	//cout << "Terminated successfully" << endl;
}

void SFController::simStart() {
	asrEnabled = true;
	should_listen = true;
	robotSpeaking = false;
	always_listen = true;
	refresh_date();
	openOutput();
	startDecoder();
	//decoder->setLM("dialogue", 0);
	startSource();
	waitForSourceFinish();
	waitForDecoderFinish();
}
}




int main(int argc, char *argv[]) {
	using namespace kaldi;
	using namespace std;


	//cout << "Starting my-online-controller" << endl;
	//int read_pipe = atoi(argv[0]); // the other process write

	//cerr << "Starting SF controller. This process reads input from the pipe, to allow interactively controlling the recogniser." << endl;
	
	struct sigaction sigIntHandler;

	sigIntHandler.sa_handler = SFController::handle;
	sigemptyset(&sigIntHandler.sa_mask);
	sigIntHandler.sa_flags = 0;

	sigaction(SIGINT, &sigIntHandler, NULL);

	SFController* controller = new SFController(argc, argv);
	SFController::instance = controller;

	// we have either received input from NNet or GMM decoder script.
	// we need to do different steps depending on which
	controller->my_log("Starting SF controller main");
	controller->readConfig();

	//controller->simStart();


	controller->start();

	controller->waitForFinish();
	//cerr << "Main  loop terminated" << endl;


	/*

	controller->startDecoder();

	//usleep(5000000);

	controller->startSource();



	//cout << "Started source" << endl;

	controller->waitForSourceFinish();
	controller->waitForDecoderFinish();
	*/

	//cout << "Got to here!" << endl;

	//controller->destroy();

	//cout << "sf-controller.cc Starting my-nnet-controller" << endl;

	//int read_pipe = atoi(argv[0]); // the other process write


	//exit;

	//char* startListening = argv[argc-1];
	//controller = new MyNnetController(argc, argv);


	/*pthread_t decoder_thread, controller_thread;
	int iret = pthread_create( &decoder_thread, NULL, start_decoder, NULL);
	if(iret)
{
		fprintf(stderr,"Error - pthread_create() return code: %d\n",iret);
		exit(EXIT_FAILURE);
}*/
	/*iret = pthread_create( &controller_thread, NULL, start_controller, NULL);
	if(iret)
{
		fprintf(stderr,"Error - pthread_create() return code: %d\n",iret);
		exit(EXIT_FAILURE);
}*/

	//pthread_join( decoder_thread, NULL);
	//pthread_join( controller_thread, NULL);

	//exit(0); 
	
	
}