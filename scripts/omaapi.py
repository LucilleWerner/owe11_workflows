import pandas
import requests
import simplejson
from time import sleep
from sys import argv

input = argv[1]
output = argv[2]

base = 'https://omabrowser.org/api/group/{}/'

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

    print(df)

    # retrieve orthologs
    df['oma'].apply(oma_call, 1)
    # add list with orthologs to df
    df['orthologs'] = ortholist

    df.to_csv(path_or_buf=output,sep='\t',header=True,index=False)


def read_csv(csv_path):
    df = pandas.read_csv(csv_path, sep='\t', header=0, nrows=5)
    print(df)

    return df

def oma_call(x):
    ID = x

    url = base.format(ID)

    req = do_request(url)

    orthos = list()
    if req:
        doc = req.json()
        if doc:
            members = doc['members']

            for entry in members:
                canon = entry['canonicalid']
                if canon != '':
                    orthos.append(canon)
                if len(orthos) == 10:
                    break

    orthos = ' ,'.join(orthos)

    ortholist.append(orthos)


if __name__ == '__main__':
    get_orthologs(input)
