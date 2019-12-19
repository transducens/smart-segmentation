#!/bin/bash

MYFULLPATH="$(readlink -f $0)"
CURDIR="$(dirname $MYFULLPATH)"

function analyze_corpus {
local L=$1
local C=$2
local VOC=$3
local OUT=$4
local ONLYVOC=$5
local AP=$6
local APL="$7"
local FURTHERSEGMENT="$8"

cat $C | perl $CURDIR/lowercase.perl | tee $C.lower  | tr ' ' '\n' | LC_ALL=C sort | LC_ALL=C uniq -c | sed 's:^[ ]*::' > $VOC 

if [ "$ONLYVOC" == ""  ]; then

if [ "$AP" == ""  ]; then
	cat $VOC |  cut -f 2 -d ' '  |  hunspell -d $L -m | LC_ALL=C sort -u | (egrep -v '^[[:space:]]*$' || :) |  (grep -F ' ' || :) | sed -r 's:[ ]+: :g' | LC_ALL=C sort  -t ' ' -k1,1 |  sed "s: :\t:"   > $OUT
else
	cat $VOC |  cut -f 2 -d ' ' | apertium -d $AP ${APL}-morph > $VOC.apertium
        cat $VOC |  cut -f 2 -d ' ' | paste -  $VOC.apertium | python3 $CURDIR/apertium-analysis-to-hunspell.py $FURTHERSEGMENT > $OUT
fi

fi

}
