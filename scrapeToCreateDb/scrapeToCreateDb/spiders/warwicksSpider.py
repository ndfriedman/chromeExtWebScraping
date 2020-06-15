import scrapy

#TODO change column names

class PowellsBooks(scrapy.Spider):
	name = "warwicksSpider"
	allowed_domains = ['warwicks.com/', 'www.warwicks.com']
	start_urls = ['https://www.warwicks.com/browse/book/CKB107000', 'https://www.warwicks.com/browse/book/CKB100000',
				'https://www.warwicks.com/browse/book/CKB127000', 'https://www.warwicks.com/browse/book/CKB119000',
				'https://www.warwicks.com/browse/book/CKB120000', 'https://www.warwicks.com/browse/book/CKB101000',
				'https://www.warwicks.com/browse/book/CKB029000', 'https://www.warwicks.com/browse/book/CKB030000',
				'https://www.warwicks.com/browse/book/CKB039000', 'https://www.warwicks.com/browse/book/CKB041000'
				'https://www.warwicks.com/browse/book/CKB042000', 'https://www.warwicks.com/browse/book/CKB115000',
				'https://www.warwicks.com/browse/book/CKB128000', 'https://www.warwicks.com/browse/book/CKB023000',
				'https://www.warwicks.com/browse/book/CKB117000', 'https://www.warwicks.com/browse/book/CKB117000',
				'https://www.warwicks.com/browse/book/CKB071000', 'https://www.warwicks.com/browse/book/CKB031000',
				'https://www.warwicks.com/browse/book/CKB077000', 'https://www.warwicks.com/browse/book/CKB105000',
				'https://www.warwicks.com/browse/book/CKB082000', 'https://www.warwicks.com/browse/book/CKB125000',
				'https://www.warwicks.com/browse/book/CKB086000']

	#code taken from https://www.datacamp.com/community/tutorials/making-web-crawlers-scrapy-python
	#other tutorial: https://blog.scrapinghub.com/price-intelligence-with-python-scrapy-sql-pandas
	def parse(self, response):

		productName =response.xpath('//div[@class="views-field views-field-label"]//span//text()').extract()
		productAuthor =response.xpath('//div[@class="views-field views-field-author-list"]//span//text()').extract()
		productPrice =response.xpath('//div[@class="views-field views-field-fss-uc-sell-price"]//span//text()').extract()

		row_data=zip(productName,productAuthor,productPrice)
		for item in row_data:
			#create a dictionary to store the scraped info
			scraped_info = {
			    #key:value
			    'url':response.url,
			    'itemName' : item[0], #item[0] means product in the list and so on, index tells what value to assign
			    'itemAuthor' : item[1],
			    'itemPrice' : item[2],
			    'seller': 'WARWICKS'
			}

			yield scraped_info

			#TODO: this next step doesn't work YET!!
			#FIX IT

			NEXT_PAGE_SELECTOR = '//li[@class="pager-next"]//a/@href' #This is the way to select the link to the next page
	        next_page = response.xpath(NEXT_PAGE_SELECTOR).extract_first()

	        if next_page:
	            yield scrapy.Request(
	            	response.urljoin(next_page),
	            	callback=self.parse)


#scrapy crawl --set="ROBOTSTXT_OBEY=False" powellsSpider