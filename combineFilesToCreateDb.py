#written by Noah Friedman
#usage: python combineFilesToCreateDb.py filesToCombine.txt combinedBookDatabase.csv
import sys
import pandas as pd 
import re

def adjust_product_name(productName):
	x = re.sub(r'\s+', '_', str(productName))
	x = re.sub(r'\W+', '', x)
	x = x.upper()
	return x

filesToCombinePath = sys.argv[1]
outputPath = sys.argv[2]

listOfDataFrames = []
with open(filesToCombinePath) as f:
	lines = f.readlines()
	for line in lines:
		listOfDataFrames.append(pd.read_csv(line.strip('\n')))
f.close()

combinedDf = pd.concat(listOfDataFrames)

#QC steps for data
#TODO uuid and data stuff
combinedDf['product_name'] = combinedDf['product_name'].apply(lambda x: adjust_product_name(x))

#rename columns for database format
combinedDf = combinedDf.rename(columns={'product_name': 'itemName', 'product_price': 'itemPrice', 'page': 'url'})

print combinedDf.columns.values
#write to file
print 'writing file to ', outputPath
combinedDf.to_csv(outputPath, sep=',', index=False)

#TODO add a rename to itemName etc