import requests
import pandas


base = 'http://eggnogapi.embl.de/nog_data/html/tree/{}'
treelinks = list()


def get_trees(path):

    df = read_csv(path)
    df['eggnog'].apply(fetch_trees, 1)

    # add treelinks to the csv

    df['tree'] = treelinks

    df.to_csv('workflow.csv')

def read_csv(csv_path):
    df = pandas.read_csv(csv_path, sep='\t', header=0, nrows=5)
    print(df)

    return df


def fetch_trees(x):
    egg = x[0]

    if egg != '':
        url = base.format(egg)
        treelinks.append(url)


if __name__ == '__main__':
    get_trees('workflow.csv')
