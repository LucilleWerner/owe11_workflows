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
    """
    text mining for cooccurence of gene names in Pubmed abstracts
    :param path: input csv path
    :return:
    """
    df = read_csv(path)

    # replace NANs for functionality
    df = df.replace(np.nan, '')
    # create global list of all symbols in the df
    get_symbols(df['symbol'])

    df.apply(get_cooccurence, 1)

    print('cooccurences: {}'.format(linked_symbols))
    # add list as new column for cooccurence
    df['cooccurence'] = linked_symbols

    df.to_csv(output, header=True, index=False, sep='\t')

def read_csv(csv_path):
    """
     reading of csv input file
     :param csv_path: path of input file
     :return: pandas dataframe
     """
    df = pandas.read_csv(csv_path, sep='\t', header=0, nrows=5, dtype={'pubmed':str, 'entrez': str})

    return df

def get_symbols(col):
    # get symbols for column in the dataframe, make list global
    global symbol_list
    symbol_list = list(symbol_list)


def do_request(url, hdr=None, prms=None):
    """
      actual REST request, with check for status code
      :param url: API url
      :return: request object
      """
    try:
        r = requests.get(url, params=prms, headers=hdr)
        if r.status_code == 200:
            t = r.text
            return t
    except Exception as e:
        print(e)


def get_cooccurence(x):
    """
    text mining for cooccurence using NCBI API for retrieval of abstracts
    :param x: one item in a column of the df
    :return:
    """
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
    """
    parsing of abstracts using the global gene symbol list
    :param abs: abstact text
    :param symbol: gene symbol linked to abstract
    :return: other gene symbols
    """
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
