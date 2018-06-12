from matplotlib import pyplot
import pandas as pd
from sys import argv

input = argv[1]
output = argv[2]

seqdf = pd.read_csv(argv[1], sep='\t')
seqs = seqdf["fasta"]
IDs = seqdf["ID"]

seqlen = []
count = 0
data = {}
for seq in seqs:
    if('M' not in seq):

        id = IDs[count]
        seq = list(seq)
        num = seq.count('A')+seq.count('C')
        tot = len(seq)
        per = int((num/tot) * 100)
        data[id] = per
        seqlen.append(str(per))
    else:
        seqlen.append("No DNA")
    count += 1

names = list(data.keys())
values = list(data.values())
fig, axs = pyplot.subplots(1,1, figsize = (len(seqs),3))
axs.bar(names,values)
fig.suptitle("gc percentage")
fig.savefig(argv[2])
seqdf["gc"] = seqlen
#seqdf.to_csv(path_or_buf=argv[1], index=False, sep="\t")
