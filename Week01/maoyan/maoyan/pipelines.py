# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os


class MaoyanPipeline:
    def open_spider(self,spider):
        # 下载目录
        download_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download_files')
        download_file = os.path.join(download_path, 'maoyan_top10.csv')
        self.f = open(download_file, 'a+', encoding='utf-8')
        self.f.write('电影名称,电影类型,上映时间\n')


    def process_item(self, item, spider):
        movie_name = item['movie_name']
        movie_type = item['movie_type']
        movie_release_time = item['movie_release_time']
        line = f'{movie_name},{movie_type},{movie_release_time}\n'
        self.f.write(line)
        return item

    def close_spider(self,spider):
        self.f.close()
