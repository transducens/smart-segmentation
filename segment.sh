#! /bin/bash


MYFULLPATH="$(readlink -f $0)"
CURDIR="$(dirname $MYFULLPATH)"

. $CURDIR/common.sh
. $CURDIR/shflags

### Segment corpus ###

DEFINE_string 'corpus' '' 'Tokenized corpus to be segmented' 'c'
DEFINE_string 'model' '' 'Model directory' 'm'
DEFINE_string 'language' '' 'Language of the corpus to be segmented' 'l'
DEFINE_string 'dictionary' '' 'Path to custom Hunspell dictionary' 'd'
DEFINE_boolean 'disable_dictionary' false 'Disable dictionary and use only suffixes' 'n'
DEFINE_boolean 'longest_suffix' false 'In case of ambiguity, choose always the longest suffix' 'L'
DEFINE_string 'analyze_apertium' '' 'Path to Apertium data dir if we want to analyze with apertium' 'a'
DEFINE_string 'subsuffixes' '' 'File with instructions about how to split Apertium suffixes' 's'

FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"

set -euo pipefail

C=${FLAGS_corpus}
M=${FLAGS_model}
L=${FLAGS_language}
AP="${FLAGS_analyze_apertium}"

if [ "$L" == "kk"  ]; then
	if [ "$AP" != ""  ]; then
		L="kaz"
	else
		L="kk_KZ"
	fi
fi

D="$CURDIR/hunspell/$L.modified"
if [ "${FLAGS_dictionary}" != ""  ]; then
       D="${FLAGS_dictionary}"
fi

WORKDIR=$(mktemp -d)

if [ "${FLAGS_disable_dictionary}" == "${FLAGS_TRUE}"  ]; then
analyze_corpus "" $C $WORKDIR/voc $WORKDIR/test.analyzed "onlyvoc" "" "" ""
touch $WORKDIR/test.analyzed
else
#Analyze test corpus
analyze_corpus $D $C $WORKDIR/voc $WORKDIR/test.analyzed "" "$AP" "$L"  "${FLAGS_subsuffixes}"
fi

if [ -f "$M/morfessormodel-v2" ]; then
	MORFESSORFLAG="--morfessor_model $M/morfessormodel-v2 --coarse_atoms"
else
	MORFESSORFLAG="--morfessor_model $M/morfessormodel"
fi
if [ "${FLAGS_longest_suffix}" == "${FLAGS_TRUE}"  ]; then
	MORFESSORFLAG=""
fi

STOPWORDSFLAG=""
if [ -f "$M/stopwords" ]; then
	STOPWORDSFLAG="--stopwords $M/stopwords"
fi

#Extract splitting dictionary
python3 $CURDIR/infer-splitting-dictionary.py $STOPWORDSFLAG  $MORFESSORFLAG  --suffixes $M/suffixes --analyzed_words $WORKDIR/test.analyzed --vocabulary $WORKDIR/voc > $WORKDIR/splitting-dictionary

python3 $CURDIR/segment.py --dictionary $WORKDIR/splitting-dictionary < $C

rm -R $WORKDIR
#echo "$WORKDIR"
