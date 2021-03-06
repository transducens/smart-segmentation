import sys
from collections import defaultdict

SUFL={}
#Huck et al.'s paper
SUFL["de"]=["e","em","en","end","enheit", "enlich","er","erheit","erlich","ern","es","est","heit","ig","igend","igkeit","igung","ik","isch","keit","lich","lichkeit","s","se","sen","ses","st","ung"]
#NLTK Snowball stemmer
SUFL["es"]=[ "selas",
        "selos",
        "sela",
        "selo",
        "las",
        "les",
        "los",
        "nos",
        "me",
        "se",
        "la",
        "le",
        "lo",
         "amientos",
        "imientos",
        "amiento",
        "imiento",
        "aciones",
        "uciones",
        "adoras",
        "adores",
        "ancias",
        "log\xEDas",
        "encias",
        "amente",
        "idades",
        "anzas",
        "ismos",
        "ables",
        "ibles",
        "istas",
        "adora",
        "aci\xF3n",
        "antes",
        "ancia",
        "log\xEDa",
        "uci\xf3n",
        "encia",
        "mente",
        "anza",
        "icos",
        "icas",
        "ismo",
        "able",
        "ible",
        "ista",
        "osos",
        "osas",
        "ador",
        "ante",
        "idad",
        "ivas",
        "ivos",
        "ico",
        "ica",
        "oso",
        "osa",
        "iva",
        "ivo",
          "yeron",
        "yendo",
        "yamos",
        "yais",
        "yan",
        "yen",
        "yas",
        "yes",
        "ya",
        "ye",
        "yo",
        "y\xF3",
          "ar\xEDamos",
        "er\xEDamos",
        "ir\xEDamos",
        "i\xE9ramos",
        "i\xE9semos",
        "ar\xEDais",
        "aremos",
        "er\xEDais",
        "eremos",
        "ir\xEDais",
        "iremos",
        "ierais",
        "ieseis",
        "asteis",
        "isteis",
        "\xE1bamos",
        "\xE1ramos",
        "\xE1semos",
        "ar\xEDan",
        "ar\xEDas",
        "ar\xE9is",
        "er\xEDan",
        "er\xEDas",
        "er\xE9is",
        "ir\xEDan",
        "ir\xEDas",
        "ir\xE9is",
        "ieran",
        "iesen",
        "ieron",
        "iendo",
        "ieras",
        "ieses",
        "abais",
        "arais",
        "aseis",
        "\xE9amos",
        "ar\xE1n",
        "ar\xE1s",
        "ar\xEDa",
        "er\xE1n",
        "er\xE1s",
        "er\xEDa",
        "ir\xE1n",
        "ir\xE1s",
        "ir\xEDa",
        "iera",
        "iese",
        "aste",
        "iste",
        "aban",
        "aran",
        "asen",
        "aron",
        "ando",
        "abas",
        "adas",
        "idas",
        "aras",
        "ases",
        "\xEDais",
        "ados",
        "idos",
        "amos",
        "imos",
        "emos",
        "ar\xE1",
        "ar\xE9",
        "er\xE1",
        "er\xE9",
        "ir\xE1",
        "ir\xE9",
        "aba",
        "ada",
        "ida",
        "ara",
        "ase",
        "\xEDan",
        "ado",
        "ido",
        "\xEDas",
        "\xE1is",
        "\xE9is",
        "\xEDa",
        "ad",
        "ed",
        "id",
        "an",
        "i\xF3",
        "ar",
        "er",
        "ir",
        "as",
        "\xEDs",
        "en",
        "es",
        "os", "a", "e", "o", "\xE1", "\xE9", "\xED", "\xF3"
        ]
#aggressive stemmer from http://members.unine.ch/jacques.savoy/clef/index.html
SUFL["cs"]=["atech","ětem","atům","ech", "ich", "ích", "ého", "ěmi", "emi", "ému",
                         "ete", "eti", "iho", "ího", "ími", "imu","ách", "ata", "aty", "ých", "ama", "ami",
                         "ové", "ovi", "ými","em","es", "ém", "ím","ům", "at", "ám", "os", "us", "ým", "mi", "ou","e","i","í","ě","u","y","ů","a","o","á","é","ý",
                         "ov", "ův","in","ejš", "ějš","oušek","eček", "éček", "iček", "íček", "enek", "ének",
                         "inek", "ínek","áček", "aček", "oček", "uček", "anek", "onek",
                         "unek", "ánek","ečk", "éčk", "ičk", "íčk", "enk", "énk",
                         "ink", "ínk","áčk", "ačk", "očk", "učk", "ank", "onk",
                         "unk", "átk", "ánk", "ušk","ek", "ék", "ík", "ik","ák", "ak", "ok", "uk","k","obinec",
                         "ionář","ovisk", "ovstv", "ovišt", "ovník","ásek", "loun", "nost", "teln", "ovec", "ovík",
                         "ovtv", "ovin", "štin","enic", "inec", "itel","árn","ěnk", "ián", "ist", "isk", "išt", "itb", "írn","och", "ost", "ovn", "oun", "out", "ouš",
                         "ušk", "kyn", "čan", "kář", "néř", "ník",
                         "ctv", "stv","áč", "ač", "án", "an", "ář", "as","ec", "en", "ěn", "éř", "íř", "ic", "in", "ín",
                         "it", "iv",
                         "ob", "ot", "ov", "oň", "ul", "yn", "čk", "čn",
                         "dl", "nk", "tv", "tk", "vk",
                         "c","č","k","l","n","t"]

#From https://en.wikipedia.org/wiki/Turkish_grammar
SUFL["tr"]=[ "ler", "lar", #PLural
"mek", "me", "iş", "yiş", #Verbal nouns
"m", "im", "miz", "imiz", "n", "in", "niz" , "iniz", "i", "si", "leri",
"yim", "yiz", "iz", "sin", "siniz", "ler",  "k", "yeyim", "eyim", "yelim", "elim", "yesin","esin", "yesiniz", "esiniz", "ye", "e","yeler", "eler",
"yiniz","sin","sinler", #Indicators of person
"mekte", "meli", "ir", "er", "mez", "emez", "yemez", "ecek", "yecek", "miş", "iyor", "di", "se" , #Verbs
"yen","en","dik", #PArticipal endings
"yı","ı", "yi","i", "yu", "u", "yü" ,"ü",
"ya", "ye", "a", "e","da", "de", "ta", "te","dan", "den", "tan", "ten","nın","ın", "nin", "in", "nun", "un", "nün", "ün", #Case
"yim", "im", "sin", "yiz", "iz", "siniz", "ler",
"le", "in", "n", "iş", "ş", "t", "dir", "ir", "er", "it", "il" , "uş", "un", "dür","tır", #Voices
"mekte", "meli","me", "mez", "ymiş", "ydi", "yse"
]

lang="de"
if len(sys.argv) > 1:
    lang=sys.argv[1]
SUF=list(set(SUFL[lang]))

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
