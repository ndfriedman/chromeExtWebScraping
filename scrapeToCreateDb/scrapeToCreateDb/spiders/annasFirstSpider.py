#written by Anna Bugankova
import scrapy

#code taken from https://www.datacamp.com/community/tutorials/making-web-crawlers-scrapy-python
#other tutorial: https://blog.scrapinghub.com/price-intelligence-with-python-scrapy-sql-pandas

class annasSpider(scrapy.Spider):
	name = "annasSpider"
	allowed_domains = ['powells.com']
	start_urls = ["https://www.powells.com/category/arts-and-entertainment"]

	def parse(self, response):
		print("procesing:"+response.url)

		#CHANGE THESE
		productName =response.xpath('//div[@class="book-title-wrapper"]//text()').extract()
		productAuthor =response.xpath('//div[@class="book-author"]//text()').extract()
		productPrice =response.xpath('//div[@class="reg-price"]//text()').extract()
		productUrl = response.xpath('//div[@class="book-title-wrapper"]//h3//a/@href').extract()

		row_data=zip(productName,productAuthor,productPrice, productUrl)

		for item in row_data:
			#create a dictionary to store the scraped info
			scraped_info = {
			    #key:value
			    'itemName' : item[0], #item[0] means product in the list and so on, index tells what value to assign
			    'itemAuthor' : item[1],
			    'itemPrice' : item[2],
			    'page': "https://www.powells.com" + item[3],
			    'seller': 'Powells'
			}

			yield scraped_info


			#CHANGE THIS!
			NEXT_PAGE_SELECTOR = '//a[@class="hawk-arrowRight hawk-pageLink "]/@href'
	        next_page = response.xpath(NEXT_PAGE_SELECTOR).extract_first()
	        if next_page:
	            yield scrapy.Request(
	            	response.urljoin(next_page),
	            	callback=self.parse)
