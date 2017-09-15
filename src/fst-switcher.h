#include "feat/wave-reader.h"
#include "online2/online-nnet2-decoding.h"
#include "online2/onlinebin-util.h"
#include "online2/online-timing.h"
#include "online2/online-endpoint.h"
#include "fstext/fstext-lib.h"
#include "lat/lattice-functions.h"
#include "thread/kaldi-thread.h"

namespace kaldi {

    /**
     * Switch between Language Model FSTs at runtime
     * @param fst_dir The directory holding the pre-generated FSTs
     */
class FSTSwitcher {

public:
    
        FSTSwitcher(string fst_dir);
        
        /**
         * Delete unwanted variables
         */
	void destroy();
	
        /**
         * Get a specified FST
         * @param type The type (dialogue, questions etc.)
         * @param index The index
         * @return The FST
         */
	fst::Fst<fst::StdArc>* get_fst(string type, int index);
        
        /**
         * Get a specified Word Symbol table
         * @param type The type (dialogue, questions etc.)
         * @param index The index
         * @return The Word Symbol Table
         */
	
	fst::SymbolTable* get_word_syms(string type, int index);
protected:

	std::vector<fst::Fst<fst::StdArc>*> dialogue_fst;
	std::vector<fst::SymbolTable*> dialogue_word_syms;
	std::vector<fst::Fst<fst::StdArc>*> question_fst;
	std::vector<fst::SymbolTable*> question_word_syms;
	std::vector<fst::Fst<fst::StdArc>*> live_question_fst;
	std::vector<fst::SymbolTable*> live_question_word_syms;
	std::vector<fst::Fst<fst::StdArc>*> command_fst;
	std::vector<fst::SymbolTable*> command_word_syms;
	std::vector<fst::Fst<fst::StdArc>*> control_fst;
	std::vector<fst::SymbolTable*> control_word_syms;

	
	std::string get_filename(string fst_dir, string dialogue_type, string file, int index);
	
	void add_fst(string file, string type);
	void add_word_syms(string file, string type);

};
}




