#written by Noah Friedman
#intended to be a pipline to ingest some number of websites via spiders, then add to or create a new database

import pandas as pd
import os
import argparse
import subprocess
import signal
import time
import re

#creates spiders by filling in a templated python file
def create_spiders():
	return 0

def create_scrapy_commands(spidersList, scriptWritePath, fileWriteDir):
	spidersDf = pd.read_table(spidersList)
	d = zip(spidersDf['spiderName'], spidersDf['name'])

	lines = []
	for spiderName, name in d:
		writePath = os.path.join(fileWriteDir, name) + '.csv'
		scrapyCmd = 'scrapy crawl --set="ROBOTSTXT_OBEY=False" --set="FEED_URI"=' + writePath + ' ' + spiderName
		lines.append(scrapyCmd)

	f = open(scriptWritePath, 'w')
	for line in lines:
		f.write(line + '\n')
	f.close()

	return [l + '.csv' for l in list(spidersDf['name'])]

#a series of commands to run scrapy on our system automatically
#todo make the scraping commands be directory felxible
def run_scrapy_commands(scrapyCommandsFile, maxTime=5):

	from threading import Timer
	kill = lambda process: process.kill()

	scrapyCommands = []
	with open(scrapyCommandsFile) as f:
		scrapyCommands = [line.strip('\n') for line in f.readlines()]

	virtualEnvSetupString = 'source env/bin/activate && cd /Users/friedman/Desktop/chromeExtDatabase/scrapeToCreateDb && ' #we chain commands together here: one to activate virtualenv, one to cd to the right place, then one to run scrapy
	procs = []
	for cmd in scrapyCommands:
		p = subprocess.Popen(virtualEnvSetupString + cmd, stdout=subprocess.PIPE, shell=True,  preexec_fn=os.setsid)
		procs.append(p)

	time.sleep(maxTime) #wait timeout length before killing all subprocesses so we can move on
	print 'killing remaining subprocesses'
	for proc in procs:
		os.killpg(os.getpgid(proc.pid), signal.SIGTERM) 


#combines files into one large csv
def combine_files_for_db(scrapingResultsDir, filenames, outputPath):
	def adjust_product_name(productName):
		x = re.sub(r'\s+', '_', str(productName))
		x = re.sub(r'\W+', '', x)
		x = x.upper()
		return x

	listOfDataFrames = []
	for file in filenames:
		listOfDataFrames.append(pd.read_csv(os.path.join(scrapingResultsDir, file)))
	combinedDf = pd.concat(listOfDataFrames)

	combinedDf['itemName'] = combinedDf['itemName'].apply(lambda x: adjust_product_name(x))
	combinedDf.to_csv(outputPath, sep=',', index=False)



def main():

	parser = argparse.ArgumentParser(description='Noahs script!')
	parser.add_argument('--scrapeResultsDir', help='the directory in which the results of the scraping will end up',
		default='/Users/friedman/Desktop/chromeExtDatabase/scrapeToCreateDb/scrapeToCreateDb/scrapingResults')
	
	parser.add_argument('--spidersList', help='path to a tsv filled with spiders to run',
		default='/Users/friedman/Desktop/chromeExtDatabase/scrapeToCreateDb/scrapeToCreateDb/listOfSpiders.tsv')

	parser.add_argument('--outputDatabaseFilePath', help='path to where we will write output to',
		default='/Users/friedman/Desktop/chromeExtDatabase/combinedBookDatabase.csv')


	#INTERMEDIATE FILE PATHS
	parser.add_argument('--scrapyCommands', help='sh file that is called for scrapy',
		default='/Users/friedman/Desktop/chromeExtDatabase/scrapingCommands.txt')


	args = parser.parse_args()

	print 'creating spider'
	create_spiders()

	print 'writing .sh instructions for scrapy to', args.scrapyCommands
	filenames = create_scrapy_commands(args.spidersList, args.scrapyCommands, args.scrapeResultsDir)

	print 'running scrapy commands'
	run_scrapy_commands(args.scrapyCommands)

	print 'combining files into database'
	combine_files_for_db(args.scrapeResultsDir, filenames, args.outputDatabaseFilePath)
	#todo run the file combination script



if __name__ == '__main__':
    main()

