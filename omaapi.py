import pandas
import requests
import simplejson
from time import sleep
base = 'https://omabrowser.org/api/protein/{}/orthologs'

ortholist = list()




def do_request(url, prms=None):
    try:
        r = requests.get(url, params=prms)
        if r.status_code == 200:
            return r
    except Exception as e:
        print(e)


def get_orthologs(path):

    df = read_csv(path)

    # retrieve orthologs
    df['oma'].apply(oma_call, 1)
    # add list with orthologs to df
    df['orthologs'] = ortholist


def read_csv(csv_path):
    df = pandas.read_csv(csv_path, sep='\t', header=0, nrows=5)
    print(df)

    return df

def oma_call(x):
    ID = x

    params = {'rel_type' '1:1'}

    url = base.format(ID)

    req = do_request(url, prms=params)

    orthos = list()
    if req:
        doc = req.json()
        if doc:
            doc = doc[0:11]
            for entry in doc:
                orthos.append(entry['canonicalid'])

    orthos = ' ,'.join(orthos)

    ortholist.append(orthos)


