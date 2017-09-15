

#include "feat/wave-reader.h"
#include "online2/online-feature-pipeline.h"
#include "online2/online-gmm-decoding.h"
#include "online2/onlinebin-util.h"
#include "online2/online-timing.h"
#include "online2/online-endpoint.h"
#include "fstext/fstext-lib.h"
#include "lat/lattice-functions.h"
#include "online-audio-source.h"



namespace kaldi {
    //class MyOnlineDecoder;
    //class GenericDecoder;


    class Simulator;

    


    // note : the wav data source is intended to simulate a real, live
    // audio source. Therefore we split into chunks and send, to see
    // if the decoder can cope.

    /**
     * This data source reads from WAV files. For compatibility with Kaldi, we use
     * a wav.scp file, and the WAV file is specified by the utterance id.
     * 
     * This also reads in chunk lengths from file, enabling the class to replicate
     * a previous run exactly.
     * 
     * @param utt The utterance id
     * @param simulator The simulator instance
     */
    class SimDataSource {
    public:
        SimDataSource(Simulator *simulator);
        bool load_wav(std::string wav_basename);
        void get_chunk(int num);
        
    private:
        RandomAccessTableReader<WaveHolder>* wav_reader;
        SubVector<BaseFloat>* data;
        int32 samp_offset;
        Simulator* simulator;
    };




}


