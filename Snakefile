rule all:
    input:
        "outputs/report.xlsx"

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

rule make_gc_plot:
    message:
        "Creating plot of gc percentages..."
    input:
        "scripts/gcplot.py",
        "outputs/dfpostoma.csv"
    output:
        "outputs/gc.png"
    shell:
        "python3 {input} {output}"

rule make_report:
    message:
        "Generating report"
    input:
        "scripts/excelwriter.py",
        "outputs/dftextmined.csv",
        "outputs/gc.png"
    output:
        "outputs/report.xlsx"
    shell:
        "python3 {input} {output}"

rule cleanup:
    message:
        "Clearing outputs folder..."
    shell:
        "rm -rfv outputs/*"

rule surprise:
    message:
        "Eating some random garbage..."
    shell:
        "python3 scripts/surprise.py"

rule dag:
    message:
        "creating workflow visualization"
    output:
        "workflow.svg"
    shell:
        "snakemake -s Snakefile --dag make_report | dot -Tsvg > workflow.svg"