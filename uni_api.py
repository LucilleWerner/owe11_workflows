import pandas
import requests
import simplejson
from time import sleep
base = 'https://www.uniprot.org/uniprot/{}.xml'


funcs = list()

def init_uni(csv_path):

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

    df.to_csv('workflow.csv', header=True, sep='\t', index=False)


def do_request(url, hdr=None, prms=None):
    try:
        r = requests.get(url, params=prms, headers=hdr)
        if r.status_code == 200:
            t = r.text
            return t
    except Exception as e:
        print(e)


def read_csv(csv_path):
    df = pandas.read_csv(csv_path, sep='\t', header=0, nrows=5, dtype={'entrez': str})


    return df


def get_func(x):
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
    contact = ""  # Please set a contact email address here to help us debug in case of problems (see https://www.uniprot.org/help/privacy).

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
    init_uni('/home/sevvy/PycharmProjects/bioapis/workflow.csv')

