from operator import itemgetter, attrgetter, methodcaller
from collections import defaultdict
res_dm = "blastn_dm2hs.txt"

res_hs = "blastn_hs2dm.txt"


def parse_blast(blast_res):
    hits = [line.split() for line in open(blast_res)]
    homs = []
    for i in hits:
        homs.append((i[1], i[0], i[2], i[10]))
    best_hits_all = {}
    for rec in homs:
        if rec[0] not in best_hits_all:
            best_hits_all[rec[0]] = [(rec[1], float(rec[3].strip()))]
        else:
            best_hits_all[rec[0]].append((rec[1], float(rec[3].strip())))
    for hom, gene in best_hits_all.items():
        best_hits_all[hom] = sorted(gene, key=itemgetter(1))
    best_hits_filt = []
    for hom, gene in best_hits_all.items():
        best_gene = gene[0][0]
        low_evalue = gene[0][1]
        entry = [hom, low_evalue, best_gene]
        #entry = best_gene.append(low_evalue)
        for i in gene:
            if i[1] <= low_evalue:
                if i[0] != best_gene:
                    entry.append(i[0])
        best_hits_filt.append(entry)
    best_hits_filt = sorted(best_hits_filt, key=itemgetter(0))
    return best_hits_all, best_hits_filt





hsall, hsfilt = parse_blast(res_hs)
dmall, dmfilt = parse_blast(res_dm)

output= open("best_homologs1.txt", "w")
for i in hsfilt:
    for g in i:
        output.write(str(g)+"\t")
    output.write("\n")
output.close()

output= open("best_homologs2.txt", "w")
for i in dmfilt:
    for g in i:
        output.write(str(g)+"\t")
    output.write("\n")
output.close()


dmfilt_dic = {}
for i in dmfilt:
    dmfilt_dic[i[0]] = i[1:]
hsfilt_dic = {}
for j in hsfilt:
    hsfilt_dic[j[0]] = j[1:]

RBH = {}
for k, v in hsfilt_dic.items():
    dm_gene = k
    homs = v
    rbhoms = []
    for h in homs:
        if h in dmfilt_dic:
            if k in dmfilt_dic[h]:
                rbhoms.append(h)
    RBH[k] = rbhoms

rbh_list = []
for k, v in RBH.items():
    entry = []
    entry.append(k)
    for i in v:
        entry.append(i)
    rbh_list.append(entry)
out_list = sorted(rbh_list, key= itemgetter(0))

output= open("rbh.txt", "w")
for r in out_list:
    for s in r:
        output.write(s + "\t")
    output.write("\n")
output.close()