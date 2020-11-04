import scrapy
from scrapy import Request, Selector
from scrapy.selector import SelectorList
from ..items import CommentItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/cinema/nowplaying/beijing/']

    # def parse(self, response):
    #     pass

    def start_requests(self):
        url = self.start_urls[0]
        yield Request(url=url, callback=self.parse_main)

    def parse_main(self, response):
        m_urls = Selector(response).xpath('//ul[@class="lists"]/li[@class="list-item"]/ul/li[1]/a/@href').extract()[:15]
        for detail_url in m_urls:
            yield Request(url=detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        comment_url = Selector(response).xpath('//*[@id="comments-section"]/div[1]/h2/span/a/@href').extract_first()
        yield Request(url=comment_url, callback=self.parse_comment)

    def parse_comment(self, response):
        movie_name = Selector(response).xpath('//h1/text()').extract_first().replace('短评', '').strip()
        comments = SelectorList(Selector(response).xpath('//div[@class="comment"]').extract())
        for comment in comments:
            shorts = Selector(text=comment).xpath('//p/span/text()').extract_first()
            votes = Selector(text=comment).xpath('//h3/span[@class="comment-vote"]/span/text()').extract_first()
            stars = Selector(text=comment).xpath(
                '//h3/span[@class="comment-info"]/span[contains(@class,"rating")]/@class').extract_first()
            if stars:
                stars = stars.split()[0].replace('allstar', '').strip().replace('0', '')
            else:
                stars = 0
            comment_time = Selector(text=comment).xpath(
                '//h3/span[@class="comment-info"]/span[@class="comment-time "]/text()').extract_first()
            comment_item = CommentItem()
            comment_item['movie_name'] = movie_name
            comment_item['shorts'] = shorts
            comment_item['stars'] = stars
            comment_item['votes'] = votes
            comment_item['comment_time'] = comment_time
            yield comment_item
