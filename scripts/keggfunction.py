from bioservices.kegg import KEGG
import pandas as pd
from sys import arg

colname = "gene_id"

df = pd.read_csv("snakemake.csv")
geneset = list(df[colname])

organism = "lpl"
pathwaylist = []
k = KEGG()
for gene in geneset:
    try:
        A = k.get_pathway_by_gene(gene,organism)
        counter = 0
        for key, value in A.items():
            if counter > 0:
                valuelist += ", " + value
            else:
                valuelist = values
                counter += 1
            pathwaylist.append(valuelist)

    except:
        print("This gene is not in a pathway")
        pathwaylist.append("no pathways")
print(pathwaylist)
df["pathways"] = pathwaylist
df.to_csv(path_or_buf="snakemake.csv", index=False, sep='\t')
