# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbScraperItem(scrapy.Item):
    # define the fields for your item here like:
    no = scrapy.Field()
    title = scrapy.Field()
    genre = scrapy.Field()
    rating = scrapy.Field()
    date_published = scrapy.Field()
    duration = scrapy.Field()
    
    pass
