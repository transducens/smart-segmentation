import sys
import os
import argparse
import math
import morfessor

from collections import defaultdict
from parsing import parse_segmentation,segmentations_to_coarse_atoms

parser = argparse.ArgumentParser(description='Generates a segmentation dictionary from a set of words segmented by hunspell')
parser.add_argument('--morfessor_model',help='Morfessor model for disambiguating segmentations.' )
parser.add_argument('--suffixes',help='Suffixes for segmenting unknown words.' )
parser.add_argument('--analyzed_words',help='Words analyzed by hunspell' )
parser.add_argument('--vocabulary',help='Vocabulary of corpus to be segmented' )
parser.add_argument('--stopwords',help='Words that should never be segmented' )
parser.add_argument('--coarse_atoms',action='store_true')
args = parser.parse_args()


numKnownUnambigous=0
numKnownAmbigous=0
numUnknown=0

freqKnownUnambigous=0
freqKnownAmbigous=0
freqUnknown=0

morfessorModel=None
if args.morfessor_model:
    if args.coarse_atoms:
        io = morfessor.MorfessorIO(atom_separator="￭")
    else:
        io = morfessor.MorfessorIO()
    morfessorModel=io.read_binary_model_file(args.morfessor_model)

#Load vocabulary: we need frequencies for statistics
freqs=defaultdict(int)
with open(args.vocabulary) as freqs_f:
    for line in freqs_f:
        line=line.rstrip("\n")
        parts=line.split(" ")
        freqs[parts[1]]=int(parts[0])



stopwords=set()
if args.stopwords:
    with open(args.stopwords) as stop_f:
        for line in stop_f:
            line=line.rstrip("\n")
            stopwords.add(line)


#word -> [ segmentation1, segmentation2, ...  ]
words=dict()
with open(args.analyzed_words) as analyzed_f:
    for line in analyzed_f:
        line=line.rstrip("\n")
        parts=line.split("\t")
        word=parts[0]
        #We store everything in memory: inefficient
        segmentation=parse_segmentation( parts[1].split(" "))
        if word not in words:
            words[word]=[]
        words[word].append(segmentation)

#suffix -> [ suf, fix]
suffixes=dict()
with open(args.suffixes) as suf_f:
    for line in suf_f:
        parts=line.rstrip("\n").split("\t")
        if parts[0] not in suffixes:
            suffixes[parts[0]]=set()
        suffixes[parts[0]].add(tuple(parts[1].split(" ")))

solution=dict()
#Unambiguous segmentations
for word in words:
    if len(words[word]) == 1:
        numKnownUnambigous+=1
        freqKnownUnambigous+=freqs[word]
        solution[word]=words[word][0]
        if len(solution[word]) > 1:
            if "".join(solution[word][1:]) not in suffixes:
                suffixes["".join(solution[word][1:]) ]=set()
            suffixes["".join(solution[word][1:]) ].add(tuple(solution[word][1:]))


if morfessorModel:
    scorer=lambda x:morfessorModel.score_segmentation("".join(x),x)
else:
    scorer=lambda x: len(x[0])

#Segment ambiguous words with morfessor
for word in words:
    if len(words[word]) > 1:
        if args.coarse_atoms:
            print("Error: --coarse_atoms does not support dictionary segmentation",file=sys.stderr)
            exit(1)
        numKnownAmbigous+=1
        freqKnownAmbigous+=freqs[word]
        bestSegmentation=min(words[word], key=scorer)
        solution[word]=bestSegmentation
        print("Alternatives for: {}".format(word),file=sys.stderr)
        for alt in words[word]:
            print( " {} score:{}".format(" ".join(alt), scorer(alt) ),file=sys.stderr )
        print("Solution: {}".format(" ".join(solution[word])),file=sys.stderr)


for k in freqs:
    if k not in solution and k not in stopwords and len(k) > 2:
        numUnknown+=1
        freqUnknown+=freqs[k]
        print("Candidate segmentations for unk {}:".format(k),file=sys.stderr)
        matchingSuffixes=[ suf for suf in suffixes if k.endswith(suf) ]
        segmentations=[ [k] ]
        for suf in matchingSuffixes:
            if len(suf) < len(k):
                for tupleSegments in suffixes[suf]:
                    segmentations.append( [ k[:-len(suf)] ]+list(tupleSegments) )
        if args.coarse_atoms:
            atoms=segmentations_to_coarse_atoms(k,segmentations)
            segmentations_with_atoms=[]
            for segtt in segmentations:
                segtt_with_atoms=[]
                pAtoms=0
                for seg in segtt:
                    seg_with_atoms=[]
                    segLen=len(seg)
                    lenVisited=0
                    while lenVisited < segLen:
                        seg_with_atoms.append(atoms[pAtoms])
                        lenVisited+=len(atoms[pAtoms])
                        pAtoms+=1
                    segtt_with_atoms.append(tuple(seg_with_atoms))
                segmentations_with_atoms.append(segtt_with_atoms)
            for segtt,segtt_atoms in zip(segmentations,segmentations_with_atoms):
                print(" {}: {}".format(" ".join(segtt), morfessorModel.score_segmentation(atoms,segtt_atoms) ),file=sys.stderr)
            bestSegmentation,bestSegmentationAtoms=min(  zip(segmentations,segmentations_with_atoms),key=lambda x: morfessorModel.score_segmentation(atoms,x[1]) )

        else:
            for seg in segmentations:
                print(" {}: {}".format(" ".join(seg), scorer(seg) ),file=sys.stderr)
            bestSegmentation=min(segmentations,key=scorer)

        solution[k] = bestSegmentation
        print("Unk {} segmented as: {}".format(k," ".join(solution[k])),file=sys.stderr)

#print solution
for w in sorted(solution.keys()):
    print(w+"\t"+" ".join(solution[w]))

#Print stats
totalVoc=numUnknown+numKnownAmbigous+numKnownUnambigous
if totalVoc > 0:
    print( "Stats on vocabulary: unamb: {} ({}) amb: {} ({}) unk: {} ({}) total: {}".format(numKnownUnambigous,numKnownUnambigous*1.0/totalVoc, numKnownAmbigous,numKnownAmbigous*1.0/totalVoc, numUnknown,numUnknown*1.0/totalVoc,totalVoc) ,file=sys.stderr)
totalFreq=freqUnknown+freqKnownAmbigous+freqKnownUnambigous
if totalFreq > 0:
    print( "Stats on frequency: unamb: {} ({}) amb: {} ({}) unk: {} ({}) total: {}".format(freqKnownUnambigous,freqKnownUnambigous*1.0/totalFreq, freqKnownAmbigous,freqKnownAmbigous*1.0/totalFreq, freqUnknown,freqUnknown*1.0/totalFreq ,totalFreq) ,file=sys.stderr)
