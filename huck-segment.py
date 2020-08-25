import sys
from collections import defaultdict

SUF=["e","em","en","end","enheit", "enlich","er","erheit","erlich","ern","es","est","heit","ig","igend","igkeit","igung","ik","isch","keit","lich","lichkeit","s","se","sen","ses","st","ung"]
for line in sys.stdin:
    w=line.rstrip("\n")
    segs=set()
    initialcand=(w,[])
    cands=[initialcand]
    finalsegs=[]
    while len(cands) > 0:
        stem,sfs=cands[0]
        cands=cands[1:]
        for s in SUF:
            if stem.endswith(s):
                newstem=stem[:-len(s)]
                cands.append((newstem, [s]+sfs))
        if len(sfs) > 0:
            finalsegs.append((stem,sfs))
    #Print
    if len(finalsegs) > 0:
        finalsegs.append(initialcand)
    for stem, sfs in finalsegs:
        fullform="".join([stem]+sfs)
        print("{}\t{}".format(fullform,  " ".join(  [ "st:"+stem ] + [ "sf:"+sf+":0" for sf in sfs  ]  )  ))
