#!/bin/bash
cd /Users/friedman/Desktop/chromeExtDatabase
source env/bin/activate
cd /Users/friedman/Desktop/chromeExtDatabase/scrapeToCreateDb
scrapy crawl --set="ROBOTSTXT_OBEY=False" --set="FEED_URI"=/Users/friedman/Desktop/chromeExtDatabase/scrapeToCreateDb/scrapeToCreateDb/scrapingResults/powells.csv powellsSpider
