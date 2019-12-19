#! /bin/bash
MYFULLPATH="$(readlink -f $0)"
CURDIR="$(dirname $MYFULLPATH)"

. $CURDIR/common.sh
. $CURDIR/shflags

### Train smart segmentation model ###
DEFINE_string 'corpus' '' 'Tokenized corpus for training model' 'c'
DEFINE_string 'output' '' 'Output directory where the model is going to be stored' 'o'
DEFINE_string 'suffixes' '' 'Path to suffixes file' 's'
DEFINE_string 'stopwords' '' 'Path to stopwords file' 'p'

FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"

C=${FLAGS_corpus}
O=${FLAGS_output}

SUF=${FLAGS_suffixes}
STOP=${FLAGS_stopwords}

mkdir -p $O

#Analyze training corpus
analyze_corpus "" $C  $O/voc $O/training.analyzed "onlyvoc"

#Read external suffixes and format them
cat $SUF | sed 's: - :	:' > $O/suffixes
cat $STOP > $O/stopwords

#Generate annotated data from suffixes
#python3 $CURDIR/suffixes_corpus_to_morfessor_segmentation.py --suffixes $O/suffixes --stopwords $O/stopwords  --vocabulary $O/voc > $O/training.analyzed.tomorfessor

python3 $CURDIR/suffixes_corpus_to_morfessor_training.py --suffixes $O/suffixes --stopwords $O/stopwords  --vocabulary $O/voc  > $O/training.voc.analyzed.tomorfessor

python3 $CURDIR/segment.py --separator '￭'  --dictionary $O/training.voc.analyzed.tomorfessor < $C.lower >  $O/training.analyzed.tomorfessor

#Train morfessor model
PATH="$HOME/.local/bin:$PATH" morfessor-train -s $O/morfessormodel-v2 --atom-separator '￭' $O/training.analyzed.tomorfessor  #-A $O/training.analyzed.tomorfessor $C.lower

