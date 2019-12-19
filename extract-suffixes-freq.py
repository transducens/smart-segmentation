import sys
from parsing import parse_segmentation
from collections import defaultdict

suffixes={}
freqs=defaultdict(int)
for line in sys.stdin:
    line=line.rstrip("\n")
    parts=line.split("\t")
    word=parts[0]
    #We store everything in memory: inefficient
    segmentation=parse_segmentation( parts[1].split(" "))
    if len(segmentation) > 1:
        if "".join(segmentation[1:]) not in suffixes:
            suffixes["".join(segmentation[1:]) ]=set()
        freqs["".join(segmentation[1:])]+=1
        suffixes["".join(segmentation[1:]) ].add(tuple(segmentation[1:]))

for s in suffixes:
    for ss in suffixes[s]:
        print("{}\t{}\t{}".format(freqs[s],s," ".join(ss)))
