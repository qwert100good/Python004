# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CommentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    movie_name = scrapy.Field()
    shorts = scrapy.Field()
    stars = scrapy.Field()
    votes = scrapy.Field()
    comment_time = scrapy.Field()