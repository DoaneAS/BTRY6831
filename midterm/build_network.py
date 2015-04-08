import subprocess
import sys

# Simple command
Ref = sys.argv[1]
Re1 = sys.argv[2]
Re2 = sys.argv[3]
cindex = "bwa index "+ Ref
c1 = 'bwa bwasw '+ Ref +' '+ Re1 + ' > dm_R1.sam'
c2 = 'bwa bwasw '+ Ref +' '+ Re2 + ' > dm_R2.sam'

subprocess.call([cindex], shell=True)

subprocess.call([c1], shell=True)
subprocess.call([c2], shell=True)

R1 = {}
for line in open("dm_R1.sam"):
    if line[0] == "@":
        continue
    sl = line.strip().split('\t')
    if sl[1] == '4':
        continue
    r_id = sl[0][7:]
    flag = sl[1]
    rname = sl[2]
    pos = sl[3]
    if r_id not in R1:
        R1[r_id] = {}
    R1[r_id][rname] = flag

R2 = {}
for line in open("dm_R2.sam"):
    if line[0] == "@":
        continue
    sl = line.strip().split('\t')
    if sl[1] == '4':
        continue
    r_id = sl[0][7:]
    flag = sl[1]
    rname = sl[2]
    pos = sl[3]
    if r_id not in R2:
        R2[r_id] = {}
    R2[r_id][rname] = flag

pairs = []
for rids in R1:
    if rids not in R2:
        continue
    #pp = (R1[k1]["RNAME"], R2[k1]["RNAME"])
    for p1 in R1[rids]:
        for p2 in R2[rids]:
            if R1[rids][p1] == R2[rids][p2]:continue
            pp = (p1, p2)
            if (p2, p1) in pairs:
                ppr = (p2, p1)
                pairs.append(ppr)
            else:
                pp = (p1, p2)
                pairs.append(pp)

from collections import defaultdict

pairsn = defaultdict(int)

for ppi in pairs:
    pairsn[ppi] += 1

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