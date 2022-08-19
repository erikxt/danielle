# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from turtle import title
import scrapy


class DaniellespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    bulletinIssueTime = scrapy.Field()
    sheetName = scrapy.Field()
