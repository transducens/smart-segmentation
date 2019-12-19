import sys

def parse_apertium_analysis(word,a):
    if a.startswith("^") and a.endswith("$"):
        if a.count("^") == 1:
            parts=a[1:-1].split("/")
            if parts[0] == word:
                if len(parts) >=2:
                    if not parts[1].startswith("*"):
                        prefixes=[p.split("<")[0] for p in parts[1:] ]
                        truePrefixes=set([ p for p in prefixes if word.startswith(p) ])
                        if len(truePrefixes) > 0:
                            sol=[]
                            for p in truePrefixes:
                                if len(p) == len(word):
                                    sol.append([word])
                                else:
                                    sol.append([word[:len(p)], word[len(p):]])

                            return sol
                            
    return None


def parse_segmentation(segments):
	out=[]
	for s in segments:
		if s.startswith("st:"):
			out.append(s.split(":")[1])
		elif s.startswith("sf:"):
			parts=s.split(":")
			removeLength=int(parts[-1])
			if removeLength > 0:
				out[-1]=out[-1][:-removeLength]
			out.append(parts[1])
		elif s.startswith("pf:"):
			parts=s.split(":")
			out.append(parts[1])
		elif s.startswith("fl:"):
			#We ignore segments that do not start with a known pattern
                        pass
		else:
			out.append(s)

	return out

#Segmentations: list of segmentations from the same compound
def segmentations_to_coarse_atoms(w,segmentations):
    breaks=set()
    #A segmentation for training morfessor compatible with
    #all the segmentations compatible with the suffixes
    # is the one that contains the union of all the break points
    for segmentation in segmentations:
        p=0
        for s in segmentation:
            p+=len(s)
            breaks.add(p)
    result=[]
    prevPosition=0
    for i in range(len(w)+1):
        if i in breaks:
            result.append(w[prevPosition:i])
            prevPosition=i
    return result
