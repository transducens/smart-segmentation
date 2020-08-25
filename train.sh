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
DEFINE_boolean 'analyze_huck' false 'Analyze with a predefined set of suffixes' 'u'

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

ANALYZE_HUCK=""
if [ "${FLAGS_analyze_huck}" == "${FLAGS_TRUE}"  ]; then
  ANALYZE_HUCK="true"
fi

mkdir -p $O

#Analyze training corpus
# If suffix splitting is enabled ($ANALYZE_HUCK), the corpus is not analyzed, as it
# only needs to be analyzed at splitting time (not at training)
analyze_corpus $D $C  $O/voc $O/training.analyzed "$ANALYZE_HUCK" "$AP" "$L" "${FLAGS_subsuffixes}" ""


#Train morfessor model
GOLDFLAG=""
if [ -f "$O/training.analyzed" ]; then
  python3 $CURDIR/hunspell_to_morfessor_segmentation.py < $O/training.analyzed > $O/training.analyzed.tomorfessor
  GOLDFLAG="-A $O/training.analyzed.tomorfessor"
fi
PATH="$HOME/.local/bin:$PATH" morfessor-train -s $O/morfessormodel $GOLDFLAG $C.lower

#Write suffixes
python3 $CURDIR/extract-suffixes.py < $O/training.analyzed > $O/suffixes
