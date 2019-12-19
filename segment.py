import sys,argparse

def copy_capitalization(capitalized,segmented):
    if len(capitalized) != len(segmented.replace(" ","")):
        print("Error when segmenting '{}'".format(capitalized),file=sys.stderr)
        return capitalized
    out=[]
    iNoSpace=0
    for i,c in enumerate(segmented):
        if c != " ":
            cCap=capitalized[iNoSpace]
            if cCap.isupper():
                out.append(c.upper())
            else:
                out.append(c)
            iNoSpace+=1
        else:
            out.append(c)
    return "".join(out)


parser = argparse.ArgumentParser(description='Segments based on a dictionary')
parser.add_argument('--dictionary',help='Segmentations dictionary.' )
parser.add_argument('--separator',default=" ￭",help='Segment separator' )
args = parser.parse_args()



segmentations={}
with open(args.dictionary) as segmentations_f:
    for line in segmentations_f:
        line=line.rstrip("\n")
        parts=line.split("\t")
        segmentations[parts[0]]=parts[1]

for line in sys.stdin:
    line=line.rstrip("\n")
    toks=line.split()
    out_l=[]
    for tok in toks:
        if tok.lower() in segmentations:
            out_l.append(copy_capitalization(tok,segmentations[tok.lower()]).replace(" ",args.separator))
        else:
            out_l.append(tok)
    print(" ".join(out_l))
