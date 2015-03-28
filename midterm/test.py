import subprocess

#bwa index dm_coding.fasta
import subprocess

# Simple command
subprocess.call(['bwa index dm_coding.fasta'], shell=True)



subprocess.call(['bwa bwasw dm_coding.fasta dm_seq_R1.fastq > dm_R1.sam'], shell=True)
subprocess.call(['bwa bwasw dm_coding.fasta dm_seq_R2.fastq > dm_R2.sam'], shell=True)

R1 = {}
for line in open("dm_R1.sam"):
    if line[0] == "@":
        pass
    else:
        sl = line.split()
        QNAME = sl[0]
        FLAG = sl[1]
        RNAME = sl[2]
        POS = sl[3]
        MAPQ = sl[4]
        CIGAR = sl[5]
        SEQ = sl[9]
        if FLAG != 4 & len(QNAME) >1:
            R1[QNAME] = {"RNAME":RNAME,
                         "FLAG":FLAG,
                         "MAPQ":MAPQ,
                         "SEQ":SEQ
            }

R2 = {}
for line in open("dm_R2.sam"):
    if line[0] == "@":
        pass
    else:
        sl = line.split()
        QNAME = sl[0]
        FLAG = sl[1]
        RNAME = sl[2]
        POS = sl[3]
        MAPQ = sl[4]
        CIGAR = sl[5]
        SEQ = sl[9]
        if FLAG != 4 & len(QNAME) >2:
            R2[QNAME] = {"RNAME":RNAME,
                         "FLAG":FLAG,
                         "MAPQ":MAPQ,
                         "SEQ":SEQ
            }
R1 = {}
for line in open("dm_R1.sam"):
    if line[0] == "@":
        pass
    else:
        sl = line.split()
        QNAME = sl[0]
        FLAG = sl[1]
        RNAME = sl[2]
        POS = sl[3]
        MAPQ = sl[4]
        CIGAR = sl[5]
        SEQ = sl[9]
        if FLAG != 4 & len(RNAME) >1:
            R1[QNAME] = {"RNAME":RNAME,
                         "FLAG":FLAG,
                         "MAPQ":MAPQ,
                         "SEQ":SEQ
            }

R2 = {}
for line in open("dm_R2.sam"):
    if line[0] == "@":
        pass
    else:
        sl = line.split()
        QNAME = sl[0]
        FLAG = sl[1]
        RNAME = sl[2]
        POS = sl[3]
        MAPQ = sl[4]
        CIGAR = sl[5]
        SEQ = sl[9]
        if FLAG != 4 & len(RNAME) >1:
            R2[QNAME] = {"RNAME":RNAME,
                         "FLAG":FLAG,
                         "MAPQ":MAPQ,
                         "SEQ":SEQ
            }

###for debugging pairs and directions
pairsD = []
same_dir = [] #pairs with same direction, for debugging
for k1, v1 in R1.items():
    if k1 in R2:
        #pp = (R1[k1]["RNAME"], R2[k1]["RNAME"])
        p1, p2 = [R1[k1]["RNAME"],R1[k1]["FLAG"]], [R2[k1]["RNAME"],R2[k1]["FLAG"]]
        if p1[1] == p2[1]:
            if (p2, p1) in same_dir:
                same_dir.append((p2, p1))
            else:
                same_dir.append((p1, p2))
        if p1[1] != p2[1]: #each pair must have 1 fwd and 1 rev comp read
            if (p2, p1) in pairsD:
                pairsD.append((p2, p1))
            else:
                pairsD.append((p1, p2))
###


pairs = []
for k1, v1 in R1.items():
    if k1 in R2:
        #pp = (R1[k1]["RNAME"], R2[k1]["RNAME"])
        p1, p2 = [R1[k1]["RNAME"],R1[k1]["FLAG"]], [R2[k1]["RNAME"],R2[k1]["FLAG"]]
        if p1[1] != p2[1]:
            if (p2[0], p1[0]) in pairs:
                pairs.append((p2[0], p1[0]))
            else:
                pairs.append((p1[0], p2[0]))

##need t take care of reverse reduncies here

from collections import defaultdict

pairsn = defaultdict(int)

for ppi in pairs:
    pairsn[ppi] += 1
pairsn



#import collections
#cnt = collections.Counter(pairs)
#cnt



pairsn_s = sorted(pairsn.items(),key=lambda (k,v): v,reverse=True)
pairsn_s
fin = []
for p in pairsn_s:
    fin.append((p[0][0], p[0][1], p[1]))

from operator import itemgetter
from operator import itemgetter
s = sorted(fin, key=itemgetter(0,1))
res = sorted(s, key=itemgetter(2), reverse=True)

output = open("dmNet.txt", "w")
for r in res:
    line = "%s\t%s\t%i\n" % (r[0], r[1], r[2])
    output.write(line)
output.close()