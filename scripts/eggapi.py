import pandas
from sys import argv

input = argv[1]
output = argv[2]

base = 'http://eggnogapi.embl.de/nog_data/html/tree/{}'
treelinks = list()


def get_trees(path):
    """
    retrieval of phylogenetic trees from eggNOG
    :param path: input csv
    :return:
    """

    df = read_csv(path)
    df['eggnog'].apply(fetch_trees, 1)

    # add treelinks to the csv

    df['tree'] = treelinks

    df.to_csv(path_or_buf=output, header=True, sep='\t', index=False)

def read_csv(csv_path):
    """
    reading of csv input file
    :param csv_path: path of input file
    :return: dataframe
    """
    df = pandas.read_csv(csv_path, sep='\t', header=0, nrows=5)
    print(df)

    return df


def fetch_trees(x):
    """
    format a eggNOG link with associated eggNOG ID
    :param x: one item in a column of the df
    :return:
    """
    egg = x[0]

    if egg != '':
        url = base.format(egg)
        treelinks.append(url)


if __name__ == '__main__':
    get_trees(input)
