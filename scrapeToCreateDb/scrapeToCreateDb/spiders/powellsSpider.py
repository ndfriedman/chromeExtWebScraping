import scrapy

class PowellsBooks(scrapy.Spider):
	name = "powellsSpider"
	allowed_domains = ['powells.com']
	start_urls = ["https://www.powells.com/category/arts-and-entertainment", 'https://www.powells.com/category/biography',
	'https://www.powells.com/category/business', 'https://www.powells.com/category/calendars-notebooks-and-gifts',
	'https://www.powells.com/category/childrens-books', 'https://www.powells.com/category/computers-and-internet',
	'https://www.powells.com/category/cooking-and-food', 'https://www.powells.com/category/education',
	'https://www.powells.com/category/engineering', 'https://www.powells.com/category/fiction-and-poetry',
	'https://www.powells.com/category/health-and-self-help', 'https://www.powells.com/category/history-and-social-science',
	'https://www.powells.com/category/hobbies-crafts-and-leisure', 'https://www.powells.com/category/home-and-garden',
	'https://www.powells.com/category/humanities', 'https://www.powells.com/category/languages',
	'https://www.powells.com/category/lgbtq', 'https://www.powells.com/category/metaphysics',
	'https://www.powells.com/category/pets', 'https://www.powells.com/category/reference',
	'https://www.powells.com/category/religion', 'https://www.powells.com/category/science-and-mathematics',
	'https://www.powells.com/category/sports-and-outdoors', 'https://www.powells.com/category/transportation',
	'https://www.powells.com/category/travel', 'https://www.powells.com/category/young-adult']

	#code taken from https://www.datacamp.com/community/tutorials/making-web-crawlers-scrapy-python
	#other tutorial: https://blog.scrapinghub.com/price-intelligence-with-python-scrapy-sql-pandas
	def parse(self, response):

		print("procesing:"+response.url)
		productName =response.xpath('//div[@class="book-title-wrapper"]//text()').extract()
		productAuthor =response.xpath('//div[@class="book-author"]//text()').extract()
		productPrice =response.xpath('//div[@class="reg-price"]//text()').extract()

		row_data=zip(productName,productAuthor,productPrice)
		for item in row_data:
			#create a dictionary to store the scraped info
			scraped_info = {
			    #key:value
			    'url':response.url,
			    'itemName' : item[0], #item[0] means product in the list and so on, index tells what value to assign
			    'itemAuthor' : item[1],
			    'itemPrice' : item[2],
			    'seller': 'POWELLS' 
			}

			yield scraped_info


			#TODO: this next step doesn't work YET!!
			#FIX IT


			#<a href="https://www.powells.com/category/arts-and-entertainment?pg=2" id="ctl00_SearchBody_NavigationBottom_lnkNext"
			#//div[@id="images"]
			NEXT_PAGE_SELECTOR = '//a[@class="hawk-arrowRight hawk-pageLink "]/@href'
	        next_page = response.xpath(NEXT_PAGE_SELECTOR).extract_first()
	        if next_page:
	            yield scrapy.Request(
	            	response.urljoin(next_page),
	            	callback=self.parse)


#to run call
'scrapy crawl --set="ROBOTSTXT_OBEY=False" powellsSpider'
#to activate call
'source env/bin/activate'

