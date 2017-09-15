#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
./interactive_yarp.sh || exit 1;
#./static_yarp.sh || exit 1;
