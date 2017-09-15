#include "feat/wave-reader.h"
#include "online2/online-feature-pipeline.h"
#include "online2/online-gmm-decoding.h"
#include "online2/onlinebin-util.h"
#include "online2/online-timing.h"
#include "online2/online-endpoint.h"
#include "fstext/fstext-lib.h"
#include "lat/lattice-functions.h"

//#include "my-online-config.h"
//#include "my-online-decoder.h"
//#include "my-online-data-source.h"
//#include "my-online-output.h"
//#include "my-online-listener.h"
//#include "my-online-simulator.h"
//#include "my-interactive-decoder.h"
//#include "generic-listener.h"
//#include "generic-decoder.h"
//#include "my-nnet-decoder.h"
//#include "my-nnet-listener.h"
//#include "my-nnet-config.h"
//#include "my-nnet-simulator.h"

//#include "sf-simulator.h"

#include "sf-sim-data-source.h"
#include "simulator.h"

#include "sf-generic-config.h"
#include "sf-decode-config.h"

#include "sf-output.h"
#include "sf-generic-decoder.h"
#include "sf-nnet-decoder.h"
#include "sf-gmm-decoder.h"
#include "fst-switcher.h"
#include "RingBuffer.h"

#define NUM_EXTRA_ARGS 8
// Yarp wrapper later


