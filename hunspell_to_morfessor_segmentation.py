import parsing
import sys

curWord=None
segmentations=[]

for line in sys.stdin:
	line=line.rstrip("\n")
	parts=line.split("\t")
	word=parts[0]
	segmentation=parsing.parse_segmentation(parts[1].split(" "))
	if word != curWord and curWord != None:
		segmentations_str=[" ".join(s) for s in segmentations]
		print(curWord+" "+", ".join(segmentations_str))
		segmentations=[]
	segmentations.append(segmentation)
	curWord=word

if len(segmentations)> 0:
	segmentations_str=[" ".join(s) for s in segmentations]
	print(word+" "+", ".join(segmentations_str))
