# Used to pull data from the tables on the https://libraries.tas.gov.au/archive-heritage/guides-records/Pages/Immigrant-ships.aspx page and writes them to a file

#!/bin/bash/python3
from lxml import html

f = open("ships.html","r")
tree = html.parse(f)
year = ""
outFile = open("ships.csv","w")

for i in range(970):
  print("row:", str(i))
  for j in range(5):
    if j==0:
      if tree.xpath('//td[@id="_td' + str(i) + '_' + str(j) + '"]/strong'):
        break
    if j == 1:
      if tree.xpath('//td[@id="_td' + str(i) + '_' + str(j) + '"]/em/text()'):
        cellContents = tree.xpath('//td[@id="_td' + str(i) + '_' + str(j) + '"]/em/text()')[0]
      elif tree.xpath('//td[@id="_td' + str(i) + '_' + str(j) + '"]/text()'):
        cellContents = tree.xpath('//td[@id="_td' + str(i) + '_' + str(j) + '"]/text()')[0]
    else:
      cellContents = tree.xpath('//td[@id="_td' + str(i) + '_' + str(j) + '"]/text()')[0]
    if j==0:
      if cellContents[0].isdigit():
        year = cellContents[:4]
        cellContents.replace("\n", "")
        outFile.write(cellContents + ",")
      else:
        outFile.write(year + ": " + cellContents+ ",")
    else:
      outFile.write(cellContents + ",")

f.close()
outFile.close()
