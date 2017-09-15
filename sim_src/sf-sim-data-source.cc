#include "my-online.h"

#include <algorithm>


namespace kaldi {
	SimDataSource::SimDataSource(Simulator *simulator) {
		std::string wav_rspecifier("scp:wav_consent.scp");
		this->wav_reader = new RandomAccessTableReader<WaveHolder>(wav_rspecifier);
		this->simulator = simulator;
	}

	void SimDataSource::get_chunk(int32 chunk_length) {
		using namespace std;
		//cout << "Reading chunk " << num << endl;
	//	int32 chunk_length = 8000;
		//int32 samp_remaining = data->Dim() - samp_offset;
		//int32 num_samp = chunk_length < samp_remaining ? chunk_length
		  //               : samp_remaining;
		stringstream ss;
		ss << "get_chunk " << chunk_length;
		string str = ss.str();
		simulator->my_log(str);
		SubVector<BaseFloat> wave_part(*data, samp_offset, chunk_length);
		Vector<BaseFloat> vec(wave_part);
		simulator -> hear(&vec);
		//cout << "Made 2nd sub vector " << endl;
		//simulator->hear(&wave_part);
		samp_offset += chunk_length;
		
		//cout << "num_samp " << num_samp << endl;
		//float wait_time = 1000000.0 * num_samp / 16000.0;
		//cout << "waiting " << wait_time << endl;
		//usleep(wait_time);
		//if (samp_offset >= data->Dim()) {
			// no more input. flush out last frames
		//	simulator->input_finished();
		//}
	}
	
	bool SimDataSource::load_wav(std::string wav_basename) {
		using namespace std;
		//cout << "Loading wav " << wav_basename << endl;
		if (wav_reader->HasKey(wav_basename)) {
			const WaveData &wave_data = wav_reader->Value(wav_basename);
			data = new SubVector<BaseFloat>(wave_data.Data(), 0);
			samp_offset = 0;
			return true;
		}
		else return false;
		
	}
	

	

}



