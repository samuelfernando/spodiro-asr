#include "my-online.h"
#include <stdlib.h>
#include <map>
namespace kaldi {


string FSTSwitcher::get_filename(string fst_dir, string dialogue_type, string file, int index) {
	using namespace std;
	ostringstream ss;
	ss.clear();
	ss << fst_dir << "/" << dialogue_type << "/graph-" <<  index << "/" << file;
	string filename = ss.str();
	return filename;
}

void FSTSwitcher::add_fst(string file, string type) {
	using namespace fst;
	fst::Fst<fst::StdArc> * decode_fst = ReadFstKaldi(file);
	if (type=="dialogue") {
		dialogue_fst.push_back(decode_fst);
	}
	else if (type=="question") {
		question_fst.push_back(decode_fst);
	}
	else if (type=="live_question") {
		live_question_fst.push_back(decode_fst);
	}
	else if (type=="commands") {
		command_fst.push_back(decode_fst);
	}
	else if (type=="controls") {
		control_fst.push_back(decode_fst);
	}

}


void FSTSwitcher::add_word_syms(string file, string type) {
	using namespace fst;
	fst::SymbolTable * word_syms = fst::SymbolTable::ReadText(file);
	if (type=="dialogue") {
		dialogue_word_syms.push_back(word_syms);
	}
	else if (type=="question") {
		question_word_syms.push_back(word_syms);
	}
	else if (type=="live_question") {
		live_question_word_syms.push_back(word_syms);
	}
	else if (type=="commands") {
		command_word_syms.push_back(word_syms);
	}
	else if (type=="controls") {
		control_word_syms.push_back(word_syms);
	}

}


FSTSwitcher::FSTSwitcher(string fst_dir) {
	using namespace fst;

	std::ifstream ifs;
	ifs.open ("fst_config_gen.txt", std::ifstream::in);
	
	if (ifs.fail()) {
		cerr << "Failed to open fst_config_gen.txt" << endl;
		std::exit(0);
	}
	std::string type;
	int no;
	//char c = ifs.get();
	cerr << "About to start reading FSTs" << endl;
	std::map<std::string,int> config;
	while (ifs >> type >> no) {
		cerr << "FST got " << type << " " << no << endl;
		config[type] = no;
	}
	
	for (int i=0;i<config["dialogue"];++i) {

		string fst_file = get_filename(fst_dir, "dialogue", "HCLG.fst", i);
		string word_syms_file = get_filename(fst_dir, "dialogue",  "words.txt", i);
		add_fst(fst_file, "dialogue");
		add_word_syms(word_syms_file, "dialogue");
	}

	for (int i=0;i<config["live_questions"];++i) {

		string fst_file = get_filename(fst_dir, "live_questions", "HCLG.fst", i);
		string word_syms_file = get_filename(fst_dir, "live_questions",  "words.txt", i);
		add_fst(fst_file, "live_question");
		add_word_syms(word_syms_file, "live_question");
	}

	for (int i=0;i<config["questions"];++i) {
		string fst_file = get_filename(fst_dir, "questions", "HCLG.fst", i);
		string word_syms_file = get_filename(fst_dir, "questions",  "words.txt", i);
		add_fst(fst_file, "question");
		add_word_syms(word_syms_file, "question");

	}
	
	for (int i=0;i<config["commands"];++i) {
		string fst_file = get_filename(fst_dir, "commands", "HCLG.fst", i);
		string word_syms_file = get_filename(fst_dir, "commands",  "words.txt", i);
		add_fst(fst_file, "commands");
		add_word_syms(word_syms_file, "commands");

	}
	for (int i=0;i<config["controls"];++i) {
		cerr << "init for controls " << i << endl;
		string fst_file = get_filename(fst_dir, "controls", "HCLG.fst", i);
		string word_syms_file = get_filename(fst_dir, "controls",  "words.txt", i);
		add_fst(fst_file, "controls");
		add_word_syms(word_syms_file, "controls");

	}
	
}

fst::Fst<fst::StdArc>* FSTSwitcher::get_fst(string type, int index) {
	if (type=="dialogue") {
		return dialogue_fst[index];
	}
	else if (type=="questions") {
		return question_fst[index];
	}
	else if (type=="live_questions") {
		return live_question_fst[index];
	}
	else if (type=="commands") {
		return command_fst[index];
	}
	else if (type=="controls") {
		return control_fst[index];
	}
	else {
		KALDI_ERR << "Wrong fst type in FST switcher!  " << type;
		return NULL;
	}
}

fst::SymbolTable* FSTSwitcher::get_word_syms(string type, int index) {
	if (type=="dialogue") {
		return dialogue_word_syms[index];
	}
	else if (type=="questions") {
		return question_word_syms[index];
	}
	else if (type=="live_questions") {
		return live_question_word_syms[index];
	}
	else if (type=="commands") {
		return command_word_syms[index];
	}
	else if (type=="controls") {
		return control_word_syms[index];
	}
	else {
		KALDI_ERR << "Wrong word syms type in FST switcher!" << type;
		return NULL;
	}
}

void FSTSwitcher::destroy() {
	//cout << "nnet config destroy " << endl;
	delete &dialogue_fst;
	delete &dialogue_word_syms;
	delete &question_fst;
	delete &question_word_syms;
	delete &live_question_fst;
	delete &live_question_word_syms;
	delete &control_word_syms;
	delete &control_fst;

}

}

/*
int main(int argc, char *argv[]) {
	using namespace kaldi;
	using namespace std;
	
	
	
	
	FSTSwitcher* fst_switch = new FSTSwitcher("grammar/jsgf-dialogue");
	fst::Fst<fst::StdArc>* fst = fst_switch -> get_fst("dialogue", 1);
	fst::SymbolTable* word_syms = fst_switch -> get_word_syms("dialogue", 1);
	
	fst->Write("out.fst");
	word_syms -> WriteText("out.syms");
	
	
}*/


