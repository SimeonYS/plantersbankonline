import re
import scrapy
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import PlantersbankonlineItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class PlantersbankonlineSpider(scrapy.Spider):
	name = 'plantersbankonline'
	start_urls = ['https://www.plantersbankonline.com/news.aspx']

	def parse(self, response):
		post_links = response.xpath('//div[@id="subPagesC"]//*[not(ancestor::div[@id="footer"] | ancestor::table)]').getall()
		flag = False
		content = []
		title = ''
		date = ''
		for el in post_links[1:]:
			tag = el[1:3]
			if tag == 'h2':
				flag = True
				if title:
					content = [p.strip() for p in content if p.strip()]
					content = re.sub(pattern, "", ' '.join(content))

					item = ItemLoader(item=PlantersbankonlineItem(), response=response)
					item.default_output_processor = TakeFirst()

					item.add_value('title', title)
					item.add_value('link', response.url)
					item.add_value('content', content)
					item.add_value('date', date)

					yield item.load_item()
				content = []
				title = remove_tags(el)

			elif tag == 'p>' and flag:
				date = remove_tags(el)
				flag = False

			else:
				content.append(remove_tags(el))

		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=PlantersbankonlineItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
