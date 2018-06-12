rule all:
    input:
        "outputs/dftextmined.csv"
rule get_data_from_ncbi:
    message:
        "Fetching data from Ncbi..."
    input:
        "scripts/ncbi_api.py",
        "RNA-Seq-counts.txt"
    output:
        "outputs/initdf.csv"
    shell:
        "python3 {input} {output}"

rule get_data_from_uniprot:
    message:
        "Fetching data from uniprot..."
    input:
        "scripts/uni_api.py",
        "outputs/initdf.csv"
    output:
        "outputs/dfpostuniprot.csv"
    shell:
        "python3 {input} {output}"

rule get_data_from_eggnog:
    message:
        "Fetching data from eggnog..."
    input:
        "scripts/eggapi.py",
        "outputs/dfpostuniprot.csv"
    output:
        "outputs/dfposteggnog.csv"
    shell:
        "python3 {input} {output}"

rule get_data_from_oma:
    message:
        "Getting orthologs..."
    input:
        "scripts/omaapi.py",
        "outputs/dfposteggnog.csv"
    output:
        "outputs/dfpostoma.csv"
    shell:
        "python3 {input} {output}"

rule mine_text:
    message:
        "Mining for co-occurence of abstracts..."
    input:
        "scripts/text_mining.py",
        "outputs/dfpostoma.csv"
    output:
        "outputs/dftextmined.csv"
    shell:
        "python3 {input} {output}"
