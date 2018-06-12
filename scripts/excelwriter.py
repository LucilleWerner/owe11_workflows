import pandas as pd
from sys import argv

input = argv[1]
imagename = argv[2]
output = argv[3]

df = pd.read_csv(argv[1], sep='\t')
writer = pd.ExcelWriter(output,engine='xlsxwriter')
df.to_excel(writer, sheet_name="rapport")

workbook = writer.book
worksheet = writer.sheets['rapport']
worksheetimage = workbook.add_worksheet('gcplot')
worksheetimage.insert_image('A1',imagename)
