import pandas
import requests
import simplejson
from time import sleep
from sys import argv
base = 'https://www.uniprot.org/uniprot/{}.xml'

input = str(argv[1])
output = str(argv[2])

funcs = list()

def init_uni(csv_path):
    """
    Uniprot API module
    :param csv_path: input csv
    :return:
    """
    df = read_csv(csv_path)

    df['entrez'].apply(get_func, 1)
    # add the new function column
    df['function'] = funcs

    # get uniprot ids
    df = id_convert(df, 'entrez', 'uniprot', 'P_ENTREZGENEID', 'ACC')
    # get eggnog ids
    df = id_convert(df, 'uniprot', 'eggnog', 'ACC', 'EGGNOG_ID')
    # get oma ids
    df = id_convert(df, 'uniprot', 'oma', 'ACC', 'OMA_ID')

    print(df.head(5))

    df.to_csv(output, header=True, sep='\t', index=False)


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


def read_csv(csv_path):
    """
    reading of csv input file
    :param csv_path: path of input file
    :return: dataframe
    """
    df = pandas.read_csv(csv_path, sep='\t', header=0, nrows=5, dtype={'entrez': str})

    return df


def get_func(x):
    """
    retrieval of gene function for Uniprot
    :param x: one item in a column of the df
    :return:
    """
    UID = x
    base = 'https://www.uniprot.org/uniprot/'
    params = {
        'query': '',
        'sort': 'score',
        'columns': 'id,go(molecular function)',
        'format': 'tab'

    }
    params['query'] = UID
    print(params)
    text = do_request(base, prms=params)

    if text:
        results = text
        # get second row (first result)
        results = results.split('\n')[2]
        func = results.split('\t')
    else:
        func = ''

    funcs.append(func)


def id_convert(df, from_col, to_col, from_db, to_db):
    """
    generic function for gene ID conversion
    :param df: dataframe
    :param from_col: name of column original ID
    :param to_col: name of column mapped ID
    :param from_db: name of original ID database
    :param to_db: name of mapped ID database
    :return: updated dataframe
    """
    # create new column for uniprot ids
    df[to_col] = ['' for _ in range(df.shape[0])]
    entrez_ids = df[from_col]
    entrez_string = ' '.join(list(entrez_ids))

    url = 'http://www.uniprot.org/uploadlists/'

    params = {
        'from': from_db,
        'to': to_db,
        'format': 'tab',
        'query': entrez_string
    }

    t = do_request(url, prms=params)

    # iterate gene entrez ids, add
    results = t.split('\n')

    if to_col == 'uniprot':
        mapped_idx = 2
    else:
        mapped_idx = 1

    if len(results) > 2:
        results = results[1:]
        results = [i.split('\t') for i in results if i!= '']
        for i, acc in enumerate(df[from_col]):
            for ri, cols in enumerate(results):
                ref = cols[0]
                mapped = cols[mapped_idx]
                if acc == ref:
                    df[to_col][i] = mapped
                    results.pop(ri)
    return df



if __name__ == '__main__':
    init_uni(input)
