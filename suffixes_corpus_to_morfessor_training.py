import sys
import os
import argparse
import math
import morfessor

from collections import defaultdict
from parsing import parse_segmentation,segmentations_to_coarse_atoms

parser = argparse.ArgumentParser(description='Generates a segmenation dictionary to be used to train a Morfessor model')
parser.add_argument('--suffixes',help='Suffixes for segmenting unknown words.' )
parser.add_argument('--stopwords',help='Words analyzed by hunspell' )
parser.add_argument('--vocabulary',help='Vocabulary of corpus to be segmented' )
args = parser.parse_args()


numKnownUnambigous=0
numKnownAmbigous=0
numUnknown=0

freqKnownUnambigous=0
freqKnownAmbigous=0
freqUnknown=0


#Load vocabulary: we need frequencies for statistics
freqs=defaultdict(int)
with open(args.vocabulary) as freqs_f:
    for line in freqs_f:
        line=line.rstrip("\n")
        parts=line.split(" ")
        freqs[parts[1]]=int(parts[0])


#suffix -> [ suf, fix]
suffixes=dict()
with open(args.suffixes) as suf_f:
    for line in suf_f:
        parts=line.rstrip("\n").split("\t")
        if parts[0] not in suffixes:
            suffixes[parts[0]]=set()
        suffixes[parts[0]].add(tuple(parts[1].split(" ")))

stopwords=set()
with open(args.stopwords) as stop_f:
    for line in stop_f:
        line=line.rstrip("\n")
        stopwords.add(line)


solution={}
for k in freqs:
    if k not in stopwords and len(k) > 2:
        numUnknown+=1
        freqUnknown+=freqs[k]
        print("Candidate segmentations for unk {}:".format(k),file=sys.stderr)
        matchingSuffixes=[ suf for suf in suffixes if k.endswith(suf) ]
        if len(matchingSuffixes) > 0:
            segmentations=[ [k] ]
            for suf in matchingSuffixes:
                for tupleSegments in suffixes[suf]:
                    if len(suf) < len(k):
                        segmentation=[ k[:-len(suf)] ]+list(tupleSegments)
                        print(" "+" ".join(segmentation),file=sys.stderr)
                        segmentations.append( segmentation )
            solution[k] = segmentations

#print solution
for w in sorted(solution.keys()):
    segmentations=solution[w]
    result=segmentations_to_coarse_atoms(w,segmentations)
    print(w+"\t"+ " ".join(result))

#Print stats
totalVoc=numUnknown+numKnownAmbigous+numKnownUnambigous
if totalVoc > 0:
    print( "Stats on vocabulary: unamb: {} ({}) amb: {} ({}) unk: {} ({}) total: {}".format(numKnownUnambigous,numKnownUnambigous*1.0/totalVoc, numKnownAmbigous,numKnownAmbigous*1.0/totalVoc, numUnknown,numUnknown*1.0/totalVoc,totalVoc) ,file=sys.stderr)
totalFreq=freqUnknown+freqKnownAmbigous+freqKnownUnambigous
if totalFreq > 0:
    print( "Stats on frequency: unamb: {} ({}) amb: {} ({}) unk: {} ({}) total: {}".format(freqKnownUnambigous,freqKnownUnambigous*1.0/totalFreq, freqKnownAmbigous,freqKnownAmbigous*1.0/totalFreq, freqUnknown,freqUnknown*1.0/totalFreq ,totalFreq) ,file=sys.stderr)
