import scrapy
import pandas as pd
import re
import string
import os
class FarfetchItem(scrapy.Item):
    name = scrapy.Field()
    brand = scrapy.Field()
    price = scrapy.Field()
    image_urls = scrapy.Field()
    prod_url = scrapy.Field()


class shoeSpider(scrapy.Spider):
	name = "blue"
	#base_link = 'https://www.blue-tomato.com'
	start_urls = ['https://www.blue-tomato.com/de-DE/products/categories/Snowboard+Shop-00000000/']
	custom_settings={
		'CONCURRENT_REQUESTS_PER_DOMAIN':1
		}

	def parse(self, response):
		na = []
		prod = []
		pr = [] 
		br = []
		k = response.xpath("//span[@class='productdesc']")
		item = FarfetchItem()		
		for j in range(len(k)):
			na.append(k.xpath("//a/@data-productname")[j].extract())
			if k.xpath("//span[@class='price']/text()")[j].extract() is not None:
				pr.append(k.xpath("//span[@class='price']/text()")[j].extract())
			elif k.xpath("//span[@class='price sale']/text()")[j].extract() is not None:
				pr.append(k.xpath("//span[@class='price sale']/text()")[j].extract())
			else:
				pr.append('null')
			br.append(k.xpath("//a/@data-brand")[j].extract())


		item['name'] = na
		item['price'] = pr
		item['prod_url']= response.xpath("//span[@class='productdesc']/a/@href").extract()
		item['brand'] = br
		waste_link = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII='
		ik = response.xpath("//section[@class='listing']")
		img = ik.xpath("//span[@class='productimage']")
		imgs = []
		for i in range(len(img)):
			imgs.append(img.xpath("//img[@width='178']/@src")[i].extract())
		ims = []
		for i in range(len(imgs)):
			if imgs[i]!= waste_link:
				ims.append('https:' + imgs[i])
			else:
				ims.append('https:' + img.xpath("//img[@width='178']/@data-src")[i].extract())
		item['image_urls'] = ims
		yield item

		next_page = response.xpath("//li[@class='next browse']/a/@href").extract_first()
		if next_page is not None:
			next_page_link = response.urljoin(next_page)
			yield scrapy.Request(url=next_page_link, callback=self.parse)

		