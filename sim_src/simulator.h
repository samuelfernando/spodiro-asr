
#include <queue>

namespace kaldi {
//class MyOnlineDecoder;
class SFGenericConfig;
class SFDecodeConfig;
class SFGenericDecoder;
class SFOutput;
class DataSource;
class RingBuffer;

/**
* This is the main class for the Simulator.
*/
class Simulator {
	friend class SimDataSource;
	friend class SFGenericDecoder;
public:
	/**
	* This is the constructor, initialised with the same arguments that
	* are passed to the main function (this makes it easier to deal with
	* all the arguments and parameters in a similar way to the Kaldi scripts).
	*/
	Simulator(int argc, char * argv[]);
	

	
	//char* getDecodeType();
	
	/**
	* Logging function, convenient method for any function to write a 
	* time-logged message.
	*/
	
	void my_log(string s);
	
	/**
	* Updates date_string and day_string to the correct values
	*/
	void refresh_date();
	
	/**
	* Reads configuration files
	*/
	void readConfig();
	
	/**
	* Start capturing audio from source 
	*/
	//void startSource();

/**
Start the simulator
*/
	void simStart();
	
	void read_file();
	
	/**
	* Start decoding. This pulls audio from the source and runs it
	* through the decoder - which could be either the GMM or the
	* DNN decoder depending on the configuration setup.
	*/
	
	void startDecoder();
	
	/**
	* This is a convenience function that waits for the simulator thread
	* to finish - calls pthread_join
	*/
	void waitForFinish();
	
	
	
	/**
	* This is a convenience function that waits for the decoder thread
	* to finish - calls pthread_join
	*/
	void waitForDecoderFinish();
	
	/**
	* This writes the current time in the format d-m-Y-H:M:S:sss to millisecond
	* level accuracy
	*/
	void get_timestamp(char* time);
	
	/**
	* This opens new output files for logging
	*/
	void openOutput();
	
	/**
	* Gets the current date as a string format: d_m_Y_H_M_S
	*/
	std::string get_date_string();

	/**
	* Gets the current day as a string format: d_m_Y
	*/
	std::string get_day_string();
	
	/**
	* Deletes unused variables 
	*/
	void destroy();
	
	/**
	* This static function terminates the thread - used by the Keyboard
	* interrupt handler to allow the thread to be terminated by a Ctrl+C
	* terminator in a Linux command terminal
	*/
	static void handle(int s);
	
	/**
	* Stops the running source and decoder threads. However - does NOT
	* stop listening for outside events - this ensures that the threads
	* started up again by a new trigger (e.g. "New person" button from
	* the GUI).
	*/
	void terminate();
	
	/**
	* This variable indicates if the robot/computer is currently speaking;
	* if so, then the ASR can switch off, to prevent it recognising the robot voice
	*/
	bool robotSpeaking;
	
	/**
	* This variable indicates if the robot was previously speaking. In conjunction
	* with robotSpeaking, we can tell if there has been a change in the variable,
	* which can trigger other processing. In this case if the robot has stopped speaking
	* we read back a short segment of audio - this is because there is a delay in 
	* receiving the end-of-speech message from the Zeno robot. 
	*/
	bool prevRobotSpeaking;
	
	/**
	* This variable indicates if the robot should listen - regardless of whether the
	* robot is speaking or not. This is used when the robot speaks several utterances
	* consecutively over a period of time, and we want to switch off listening completely.
	* Without this, we would get small segments of audio seeping in between the utterances.
	*/
	bool should_listen;
	
	/**
	* This is used by the command and control application where we want the system
	* to always listen.
	*/
	bool always_listen;
	
	/**
	* Singleton instance of the simulator which can be used by static functions.
	*/
	static Simulator* instance;
	
	/**
	* Given a lattice output from ASR and a word symbol table, this outputs the most likely string.
        * Delegated to sf-output.cc
	*/
	std::string output_string(fst::SymbolTable *word_syms, CompactLattice clat, int64* num_frames, double* tot_like);
	
protected:
	std::vector<std::string>& split(const std::string &s, char delim, std::vector<std::string> &elems);
	std::vector<std::string> split(const std::string &s, char delim);
	bool startswith(string prefix, string str);
	std::string *date_string;
	std::string *day_string;
	
	void add_chunk(int size);
	void hear(Vector<BaseFloat>* data);
	void input_finished();
	int read_pipe;
	//Vector<BaseFloat>* prevData;
	RingBuffer* prevData;
	bool startListening;
	int argc;
	char ** argv;
	SimDataSource* src;
	SFGenericDecoder* decoder;
	SFGenericConfig* gen_config;
	SFDecodeConfig* decode_config;
	MatrixIndexT sample_count;
	SFOutput* output;
	bool writeLock;
	bool read_back;
	int read_size;
	bool wav_active;
	std::string current_wav;
	//std::string prev_event;
	//timeval prev_event_time;
	bool asrEnabled; // i.e. not WOZ
	pthread_t* simulator_thread;
};

}

	// NEW-SF-CONTROLLER_H

