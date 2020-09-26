import scrapy
from scrapy import Request, Selector
from ..items import MaoyanItem


class MaoyanSpiderSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['movie.maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    # def parse(self, response):
    #     pass

    def start_requests(self):
        url = self.start_urls[0]
        # yield Request(url=url, callback=self.maoyan_parse, meta={'proxy':'http://104.129.196.38:8800'})
        yield Request(url=url, callback=self.maoyan_parse)

    def maoyan_parse(self, response):
        movies = Selector(response=response).xpath('//div[@class="movie-hover-info"]')
        # 前10个电影
        for movie in movies[:10]:
            movie_item = MaoyanItem()
            movie_name = movie.xpath('./div[1]/span[1]/text()').extract_first().strip()
            # ['\n              ', '\n              爱情／喜剧\n            ']
            movie_type = movie.xpath('./div[2]/text()').extract()[-1].strip()
            # ['\n              ', '\n              2020-09-11\n            ']
            movie_release_time = movie.xpath('./div[4]/text()').extract()[-1].strip()
            movie_item['movie_name'] = movie_name
            movie_item['movie_type'] = movie_type
            movie_item['movie_release_time'] = movie_release_time
            yield movie_item
