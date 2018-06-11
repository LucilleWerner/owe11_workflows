import requests
import pandas
import re
from sys import argv
from bs4 import element
from bs4 import BeautifulSoup


id_types = {
    "ensembl": 'ENS[A-Z]+[0-9]{11}|[A-Z]{3}[0-9]{3}[A-Za-z](-[A-Za-z])?'
               '|CG[0-9]+|[A-Z0-9]+\.[0-9]+|YM[A-Z][0-9]{3}[a-z][0-9]',
    "genbank": '[0-9]+',
    'locustag': '(\w){1,5}_(\d)+',
    'entrez': '[0-9]+|[A-Z]{1,2}_[0-9]+|[A-Z]{1,2}_[A-Z]{1,4}[0-9]+',
    'uniprot': ' [OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}',
    'hgnc': '^((HGNC|hgnc):)?\d{1,5}$',
    'encode': '^ENC[A-Za-z]{2}[0-9]{3}[A-Za-z]{3}$',
    'affymatrix': '\d{4,}((_[asx])?_at)?',
    'illumina': '^ILMN_[0-9]+$',
    'interpro': '^IPR\d{6}$',
    'GO': '^GO_REF:\d{7}$',

}

base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'

id_list = set()

entrez_ids = list()
fastas = list()
symbols = list()
pmids = list()


def fetch_ids(csv_path):

    df = read_csv(csv_path)
    df.apply(check_id_types, 1)

    if len(id_list) > 1:
        print('multiple ID types found: {}'.format(' '.join(id_list)))
    elif len(id_list) == 1:
        print('ID type found: {}'.format(' '.join(id_list)))
    else:
        print('No ID type found, use other ID type')

    # construct list of entrez ids
    df.apply(get_entrez_ids, 1)

    # add entrez id list to the df
    df['entrez'] = entrez_ids

    # construct list of symbols
    df['entrez'].apply(fetch_symbol, 1)

    # add list of symbols to the df
    df['symbol'] = symbols

    # get pubmed ids per gene
    df['symbol'].apply(fetch_pubmed, 1)

    # add pubmed ids to the df
    df['pubmed'] = pmids

    # fetch fasta sequences
    df['entrez'].apply(fetch_fasta, 1)

    # add fasta list to df
    df['fasta'] = fastas

    print(df.head(5))

    df.to_csv('workflow.csv', header=True, sep='\t', index=False)


def read_csv(csv_path):
    df = pandas.read_csv(csv_path, sep='\t', usecols=['ID'], header=0, skiprows=1, nrows=5)
    print(df)

    return df


def check_id_types(x):
    ID = x[0]

    for id_type in id_types:
        idregex = id_types[id_type]
        m = re.match(idregex, ID, re.I)
        if m:
            id_list.add(id_type)

def do_request(url):
    try:
        r = requests.get(url)
        while True:
            if r.status_code == 200:
               return r
            r.raise_for_status()
    except Exception as e:
        print(e)



def get_entrez_ids(x):
    ID = x[0]

    querystring = 'esearch.fcgi?db={}&{}={}'

    url = base + querystring.format('gene', 'term', ID)

    req = do_request(url)

    if req:
        doc = req.text

        soup = BeautifulSoup(doc, 'html.parser')
        id_lookup = soup.id
        if id_lookup:
            entrez = soup.id.text
        else:
            entrez = ''
    else:
        entrez = ''

    entrez_ids.append(entrez)

def fetch_symbol(x):
    ID = x
    querystring = 'esummary.fcgi?db=gene&id={}'
    url = base+querystring.format(ID)

    req = do_request(url)

    if req:
        doc = req.text
        soup = BeautifulSoup(doc, 'html.parser')
        id_lookup = soup.find('name')
        if id_lookup:
            symbol = id_lookup.text
        else:
            symbol = ''
    else:
        symbol = ''

    symbols.append(symbol)

def fetch_pubmed(x):
    symbol = x
    querystring = 'esearch.fcgi?db=pmc&term={}'
    url = base + querystring.format(symbol)

    req = do_request(url)

    if req:
        doc = req.text

        soup = BeautifulSoup(doc, 'html.parser')
        id_lookup = soup.idlist
        if id_lookup:
            ids = [i.text for i in id_lookup if isinstance(i, element.Tag)]
            ids = ', '.join(ids[0:10])
        else:
            ids = ''
    else:
        ids = ''
    pmids.append(ids)



def fetch_fasta(x):

    ID = x
    querystring = 'efetch.fcgi?db=nuccore&id={}&rettype=fasta'
    url = base + querystring.format(ID)

    req = do_request(url)

    if req:
        fasta = ''.join(req.text.split('\n')[1:])

    else:
        fasta = ''

    fastas.append(fasta)




if __name__ == '__main__':
    #
    # csv_path = argv[1]
    # fetch_ids(csv_path)

    csv_path = '/home/sevvy/Documents/owe11/bioinformatica/data/RNA-Seq-counts.txt'
    fetch_ids(csv_path)

"""
1. Genn symbolen omzetten in entrez ID's
2. Kegg API (af)
3. eggnog id's
4. orthologs via eggnog
5. eggnog phylogentic
6. GC plotjes
7. Rapport bouwert
8. asci 
9. DAG
10. excel"""

