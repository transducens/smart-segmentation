#! /bin/bash
MYFULLPATH="$(readlink -f $0)"
CURDIR="$(dirname $MYFULLPATH)"

. $CURDIR/common.sh
 . $CURDIR/shflags

### Train smart segmentation model ###

DEFINE_string 'corpus' '' 'Tokenized corpus for training model' 'c'
DEFINE_string 'output' '' 'Output directory where the model is going to be stored' 'o'
DEFINE_string 'language' '' 'Language of the corpus to be segmented' 'l'
DEFINE_string 'dictionary' '' 'Path to custom Hunspell dictionary' 'd'
DEFINE_string 'analyze_apertium' '' 'Path to Apertium data dir if we want to analyze with apertium' 'a'
DEFINE_string 'subsuffixes' '' 'File with instructions about how to split Apertium suffixes' 's'

FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"

C=${FLAGS_corpus}
O=${FLAGS_output}
L=${FLAGS_language}
AP="${FLAGS_analyze_apertium}"

if [ "$L" == "kk"  ]; then
       L="kk_KZ"
fi

D="$CURDIR/hunspell/$L.modified"
if [ "${FLAGS_dictionary}" != ""  ]; then
	D="${FLAGS_dictionary}"
fi

mkdir -p $O

#Analyze training corpus
analyze_corpus $D $C  $O/voc $O/training.analyzed "" "$AP" "$L" "${FLAGS_subsuffixes}"


#Train morfessor model
python3 $CURDIR/hunspell_to_morfessor_segmentation.py < $O/training.analyzed > $O/training.analyzed.tomorfessor
PATH="$HOME/.local/bin:$PATH" morfessor-train -s $O/morfessormodel -A $O/training.analyzed.tomorfessor $C.lower

#Write suffixes
python3 $CURDIR/extract-suffixes.py < $O/training.analyzed > $O/suffixes
