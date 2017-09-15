#include "my-online.h"
#include <signal.h>

// receives some data from the data source, and decodes it
namespace kaldi {

Simulator* Simulator::instance;

void Simulator::my_log(string s) {
	char currentTime[84];
	get_timestamp(currentTime);
	while (writeLock) {}
	
	writeLock = true;
	cerr << currentTime << " " << s << endl;
	writeLock = false;
}

void Simulator::get_timestamp(char* currentTime) {
	timeval curTime;
	gettimeofday(&curTime, NULL);
	int milli = curTime.tv_usec/1000;
	char buffer[80];
	strftime(buffer, 80, "%d-%m-%Y-%H:%M:%S", localtime(&curTime.tv_sec));
	//char currentTime[84]="";
	sprintf(currentTime, "%s:%03d", buffer, milli);
	//return currentTime;
}

Simulator::Simulator(int argc, char* argv[]) {
	this -> argc = argc;
	this -> argv = argv;
	this -> writeLock = false;
	for (int i=0;i<argc;++i) {
		//cerr << argv[i] << endl;
	}
	this -> startListening = argv[argc-2];

	this->read_pipe = atoi(argv[argc-3]);
	//cerr << "read pipe " << read_pipe << endl;
	string write = "read pipe ";
	write.append(argv[argc-3]);
	my_log(write);
	//my_buffer = new BaseFloat[8000];
	this -> should_listen = false;
	this -> always_listen = false;
	this -> sample_count = 0;
	simulator_thread = new pthread_t();
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


void Simulator::hear(Vector<BaseFloat>* data) {
	if (!wav_active) {
		return;
	}
	using namespace std;
	//cout << "simulator hear "<< data->Dim() << endl;
	MatrixIndexT start = sample_count;
	MatrixIndexT end = sample_count + data->Dim();
	sample_count += data->Dim();
	//for (int i=0;i<data->Dim();++i) {
	//	my_buffer[i] = data->Data()[i];
	//}
	
	stringstream ss;
	ss << "hear current_wav " << current_wav << " " << start << " " << end;
	string str = ss.str();
	
	my_log(str);
	
	if (read_back) {
		stringstream ss;
		ss << "Reading back " << read_size << " " << prevData->totalSize();
		
		string str = ss.str();
		my_log(str);
		
		
//		output->write_readback(read_size);
	//	output->write_readback_actual(prevData->totalSize());
		decoder->hearPrev(prevData);
		read_back = false;
	}
	
	
	if (should_listen) {
	//	while (!decoder->lm_ready) {
			//my_log("waiting for controller to be ready");
		//}
		decoder -> hear(data);
		output -> write_segment(start, end, true);
	}
	else {
		
		//cerr << "either !should_listen or robot speaking" << endl;

		//cerr << "about to write segment" << endl;

		output -> write_segment(start, end, false);
		
		/*float avg = 0.0;
		for (int j=0;j<data->Dim();++j) {
			avg+=abs(data->Data()[j]);
		}
		avg=avg/data->Dim();
		cerr << "Inserting "  << " " << avg << endl;
		*/
		
		//cerr << "writing prevData to buffer" << endl;

		prevData->insert(data);
	}
	

	
}

void Simulator::refresh_date() {
	time_t t = time(0);   // get time now
	struct tm * now = localtime( & t );
	char buffer[80];
	strftime(buffer,80,"%d_%m_%Y_%H_%M_%S",now);
	date_string = new string(buffer);
	char daybuf[80];
	strftime(daybuf,80,"%d_%m_%Y", now);
	day_string = new string(daybuf);
}

void Simulator::input_finished() {
	//cout << "input finished"<<endl;
	decoder->input_finished_func();
	decoder->stop();
	//listener -> input_finished_func();
	//listener -> stop();
}

void Simulator::add_chunk(int size) {
	//cout << "adding chunk" << endl;
	output->add_chunk(size);
}

std::string Simulator::get_date_string() {
	return *date_string;
}

std::string Simulator::get_day_string() {
	return *day_string;
}

void Simulator::startDecoder() {
	//cout << "Simulator startDecoder" << endl;
	//cout << "type" << gen_config->decode_type << endl;
	if (!strcmp(gen_config->decode_type, "nnet")) {
		//cout << "About to open the SFNnetDecoder" << endl;
		decoder = new SFNnetDecoder(this, (SFNnetConfig*)decode_config, gen_config->keyphrase);
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


	//decoder->start();
}


/*void Simulator::startSource() {
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
}*/


std::vector<std::string>& Simulator::split(const std::string &s, char delim, std::vector<std::string> &elems) {
	std::stringstream ss(s);
	std::string item;
	while (std::getline(ss, item, delim)) {
		elems.push_back(item);
	}
	return elems;
}

void Simulator::waitForFinish() {
	pthread_join( *simulator_thread, NULL);
}

std::vector<std::string> Simulator::split(const std::string &s, char delim) {
	std::vector<std::string> elems;
	split(s, delim, elems);
	return elems;
}

bool Simulator::startswith(string prefix, string str) {
	return str.substr(0, prefix.size()) == prefix;
}


void Simulator::waitForDecoderFinish() {
	decoder -> waitForFinish();
}

void Simulator::readConfig() {

	//for (int i=0;i<argc;++i) {
	//cout << argv[i] << endl;
	//}

	gen_config = new SFGenericConfig(argc, argv);

	if (!strcmp(gen_config->decode_type, "nnet")) {
		//cerr << "Loading NNET config " << NUM_EXTRA_ARGS << endl;
		my_log("Loading NNET config " + NUM_EXTRA_ARGS);
		decode_config = new SFNnetConfig(argc - NUM_EXTRA_ARGS, argv);
	}
	else {
		
		my_log("Loading GMM config " + NUM_EXTRA_ARGS); 
	//	cerr << "Loading GMM config " << NUM_EXTRA_ARGS << endl;
		decode_config = new SFGmmConfig(argc - NUM_EXTRA_ARGS, argv);

	}

}


int diff_ms(timeval t1, timeval t2)
{
    return (((t1.tv_sec - t2.tv_sec) * 1000000) + 
            (t1.tv_usec - t2.tv_usec))/1000;
}




void Simulator::destroy() {
	//cout << "Doing destroy "<<endl;
	decode_config -> destroy();
}

void Simulator::openOutput() {
	//cout << "out path " << gen_config -> output_path << endl;

	//cout << "base name " << gen_config -> base_name << endl;
	output = new SFOutput(this, gen_config->source, gen_config->base_name, gen_config->output_path);
}

string Simulator::output_string(fst::SymbolTable *word_syms, CompactLattice clat, int64* num_frames, double* tot_like) {
	//cout << " orig output " << endl;
	return output -> output_string(word_syms, clat, num_frames, tot_like, sample_count);
}

void Simulator::handle(int s) {

	Simulator::instance -> terminate();
	printf("Caught signal %d\n",s);
	//exit(1);
}

void Simulator::terminate() {
	//src -> stop();
	if (asrEnabled) {
		decoder -> stop();
	}
	my_log("Terminated successfully");
	//cout << "Terminated successfully" << endl;
}




void Simulator::simStart() {
	asrEnabled = true;
	should_listen = true;
	robotSpeaking = false;
	always_listen = true;
	refresh_date();
	openOutput();
	startDecoder();
	decoder->setLM("dialogue", 0);
	//startSource();
	//waitForSourceFinish();
	waitForDecoderFinish();
}

void Simulator::read_file() {
	//timeval time;
	using namespace std;
	src = new SimDataSource(this);
	//src -> get_chunk(800);
	
	string out_str("all_log.txt");
	std::ifstream infile(out_str.c_str());
	std::string line;
	
	out_str = "out_log.txt";
	//std::ofstream outfile;
	//outfile.open(out_str.c_str());
	refresh_date();
	
	//bool wav_active = false;
	wav_active = false;
	asrEnabled = true;
	robotSpeaking = true;
	read_back = false;
	should_listen = false;
	startDecoder();
	decoder->setLM("dialogue", 0);

	while(std::getline(infile, line)) {
		std::stringstream linestream(line);
		std::string data[8];
		for (int i=0;i<8;++i) {
			std::getline(linestream, data[i], '\t');
			//outfile << data[i] << "\t";
		}
		std::string info = data[7];
		std::stringstream infostream(info);
		std::string keyword, tmp;
		infostream >> keyword;
		if (keyword=="Control") {
			std::string base;
			int chunk_size;
			//bool should_listen;
			infostream >> base;
			infostream >> base >> tmp >> chunk_size >> should_listen;
			bool ret = src -> load_wav(base);
			if (ret) {
				wav_active = true;	
				current_wav = base;
				stringstream ss;
				
				ss << "Loading wav " << base << " chunk size " << chunk_size << " " << should_listen; 
				string str = ss.str();
				my_log(str);
				output = new SFOutput(this, gen_config->source, base.c_str(), gen_config->output_path);
				this -> sample_count = 0;
				src -> get_chunk(chunk_size);
				
			}
			else {
				wav_active = false;
				stringstream ss;
				
				ss << "Wav not in consent " << base; 
				string str = ss.str();
				my_log(str);
				
				
				//	outfile << "Wav not in consent " << base << endl; 
			}
		}
		else if (keyword=="Chunk") {
			int chunk_size;
			//bool should_listen;
			bool tmp;
			infostream >> chunk_size >> tmp;
			stringstream ss;
			ss << "Reading chunk " << chunk_size << " should_listen " << should_listen  << " wav_active " << wav_active;
			string str = ss.str();
			my_log(str);
			
			if (wav_active) {
				src -> get_chunk(chunk_size);
			}
		} else if (keyword=="Read") {
			//int read_size;
			infostream >> tmp >> read_size;
			stringstream ss;
			ss << "Back read " << read_size;
			string str = ss.str();
			my_log(str);
			
			if (wav_active) {
				read_back = true;
				should_listen = true;
			}
			
		} else if (keyword=="lm") {
			std::string type;
			int num;
			infostream >> type >> num;
			stringstream ss;
			ss << "LM change " << type << " " << num;
			string str = ss.str();
			my_log(str);
			
			decoder->setLM(type, num);
		}		
		else {
			my_log("UNKNOWN COMMAND");
			//outfile << "UNKNOWN COMMAND" << endl; 
		}
		
		//outfile << "\n";
		
	}
	//outfile.close();

}

}

int main(int argc, char *argv[]) {
	using namespace kaldi;
	using namespace std;


	//cout << "Starting my-online-simulator" << endl;
	//int read_pipe = atoi(argv[0]); // the other process write

	//cerr << "Starting SF simulator. This process reads input from the pipe, to allow interactively controlling the recogniser." << endl;
	
	struct sigaction sigIntHandler;

	sigIntHandler.sa_handler = Simulator::handle;
	sigemptyset(&sigIntHandler.sa_mask);
	sigIntHandler.sa_flags = 0;

	sigaction(SIGINT, &sigIntHandler, NULL);

	Simulator* simulator = new Simulator(argc, argv);
	Simulator::instance = simulator;

	// we have either received input from NNet or GMM decoder script.
	// we need to do different steps depending on which
	simulator->my_log("Starting SF simulator main");
	simulator->readConfig();
	
	//simulator->simStart();
	simulator->read_file();

	
	

	//simulator->start();

	//simulator->waitForFinish();

	/*

	simulator->startDecoder();

	//usleep(5000000);

	simulator->startSource();



	//cout << "Started source" << endl;

	simulator->waitForSourceFinish();
	simulator->waitForDecoderFinish();
	*/

	//cout << "Got to here!" << endl;

	//simulator->destroy();

	//cout << "sf-simulator.cc Starting my-nnet-simulator" << endl;

	//int read_pipe = atoi(argv[0]); // the other process write


	//exit;

	//char* startListening = argv[argc-1];
	//simulator = new MyNnetController(argc, argv);


	/*pthread_t decoder_thread, simulator_thread;
	int iret = pthread_create( &decoder_thread, NULL, start_decoder, NULL);
	if(iret)
{
		fprintf(stderr,"Error - pthread_create() return code: %d\n",iret);
		exit(EXIT_FAILURE);
}*/
	/*iret = pthread_create( &simulator_thread, NULL, start_simulator, NULL);
	if(iret)
{
		fprintf(stderr,"Error - pthread_create() return code: %d\n",iret);
		exit(EXIT_FAILURE);
}*/

	//pthread_join( decoder_thread, NULL);
	//pthread_join( simulator_thread, NULL);


	return 0;
}
