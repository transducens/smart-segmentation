import parsing
import sys


fs={}
if len(sys.argv)  > 1:
    with open( sys.argv[1] ) as fs_f:
        for line in fs_f:
            line=line.rstrip("\n")
            parts=line.split(" - ")
            fs[parts[0]]=parts[1]


for line in sys.stdin:
    line=line.rstrip("\n")
    word,rawa=line.split("\t")
    analyses=parsing.parse_apertium_analysis(word, rawa)
    if all(c.isalpha() for c in word) and  analyses != None:
        for a in analyses:
            a[0]="st:"+a[0]
            if len(a) > 1:
                if a[1] in fs:
                    a=[a[0]]+fs[a[1]].split(" ")
            for i in range(1,len(a)):
                a[i]="sf:"+a[i]+":0"
            print("{}\t{}".format(word," ".join(a)))

