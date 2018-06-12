import requests
import pandas
import numpy as np
from sys import argv

input = argv[1]
output = argv[2]

base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
symbol_list = list()
linked_symbols = list()


def text_mine(path):

    df = read_csv(path)

    print(df)

    df = df.replace(np.nan, '')
    print(df)
    get_symbols(df['symbol'])

    df.apply(get_cooccurence, 1)

    print('cooccurences: {}'.format(linked_symbols))
    # add list as new column for cooccurence
    df['cooccurence'] = linked_symbols

    df.to_csv(output, header=True, index=False, sep='\t')

def read_csv(csv_path):
    df = pandas.read_csv(csv_path, sep='\t', header=0, nrows=5, dtype={'pubmed':str, 'entrez': str})


    return df

def get_symbols(col):
    global symbol_list

    symbol_list = list(symbol_list)


def do_request(url, hdr=None, prms=None):
    try:
        r = requests.get(url, params=prms, headers=hdr)
        if r.status_code == 200:
            t = r.text
            return t
    except Exception as e:
        print(e)


def get_cooccurence(x):

    pmids = x['pubmed']
    symbol = x['symbol']

    pmids = pmids.split(', ')
    cooccurence = set()
    url = base + "efetch.fcgi?db=pubmed&id={}&rettype=abstract&retmode=text"


    for pmid in pmids:
        print(pmid)

        r = requests.get(url.format(pmid))

        t = r.text
        # default for cooccurence
        linked = ''
        if t:
            pars = t.split('\n\n')
            abs = [i for i in pars if len(pars) > 600]
            if abs:
                # sort on length in case more than one paragraph was found containing more than 800 tokens
                abs.sort(key=len, reverse=True)
                abs = abs[0]
                linked = parse_abs(abs, symbol)
        cooccurence.add(linked)

    cooccurence = ', '.join(cooccurence)
    linked_symbols.append(cooccurence)



def parse_abs(abs, symbol):
    linked = list()

    symbols = symbol_list
    rest_symbols = symbols.pop(symbol_list.index(symbol))
    print(rest_symbols)
    for s in rest_symbols:
        idx = abs.find(s)
        if idx != -1:
            linked.append(s)

    if linked:
        return ', '.join(linked)
    else:
        return ''



if __name__ == '__main__':
    text_mine(input)
