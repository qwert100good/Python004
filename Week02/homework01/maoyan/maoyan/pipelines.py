# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import datetime
import os

import pymysql
from itemadapter import ItemAdapter


class MaoyanPipeline:
    # def process_item(self, item, spider):
    #     return item
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

class MaoyanMySQLPipeline:
    def __init__(self,conn):
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.movie_info_list = []

    # MySQL配置存放在settings配置文件中，通过该方法读取构造mysql连接
    @classmethod
    def from_settings(cls, settings):
        db_config = dict(
            host=settings['MYSQL_HOST'],
            port=settings['MYSQL_PORT'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'])
        conn = pymysql.connect(**db_config)
        return cls(conn)

    def process_item(self,item,spider):
        movie_name = item['movie_name']
        movie_type = item['movie_type']
        movie_release_time = item['movie_release_time']
        self.movie_info_list.append([movie_name,movie_type,movie_release_time])
        return item

    def close_spider(self, spider):
        insert_sql = 'INSERT INTO movie_info(`name`,`type`,`release_time`,`create_time`) VALUES (%s,%s,%s,%s)'
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        movie_info_list = [tuple(row + [create_time]) for row in self.movie_info_list]
        try:
            self.cursor.executemany(insert_sql, movie_info_list)
            self.conn.commit()
        except:
            self.conn.rollback()
        self.cursor.close()
        self.conn.close()