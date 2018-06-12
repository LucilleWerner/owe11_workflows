# Workflows course 11
----------------------------------------------------------

This is a workflow for the annotation of proteins with a variation
of sources: NCBI, Uniprot, OMA, eggNOG and KEGG. These sources are used for:
* ID mapping: NCBI geneID, Uniprot, eggNOG
* DNA/protein sequence retrieval
* retrieval of orthologs
* text mining for cooccurence of genes in pubmed abstracts
* KEGG pathway retrieval
* GC percentage plots

### Snakemake

The workflow language Snakemake is a commenly used tool for seamless pipeline development. This project is easily extensible with more functionality because of this. Snakemake also makes it possible to visualise your workflow with a DAG (directed acyclic graph), see image below.
See the documentation:
 https://snakemake.readthedocs.io/en/stable/

### Setting things up

For this pipeline to run you only need anaconda and the installation of a conda environment.

First: anaconda, Mini conda is recommended if for minimal space usage.

##### Linux:
https://conda.io/docs/user-guide/install/linux.html

##### Windows:
https://conda.io/docs/user-guide/install/windows.html

Second: the environment, the config file is included in this repository

``` bash
conda env create -n <env name> -f conda_workflows.yaml
```

```bash
source activate <env name>
```
### Input

The input file must contain gene IDs. You can specify which column contains these IDs. The program will attempt to recognize the ID type and will perform mapping to a variety of gene IDs.


### Output

The output report contains all the gathered information in a tab separated file. CG plots will be saved in a subfolder "plots"

### The workflow
