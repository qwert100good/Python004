# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from snownlp import SnowNLP
from itemadapter import ItemAdapter


class DoubanmoviePipeline:
    def process_item(self, item, spider):
        return item


class DoubanMySQLPipeline:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.comment_list = []

    # MySQL配置存放在settings配置文件中，通过该方法读取构造mysql连接
    @classmethod
    def from_settings(cls, settings):
        db_config = dict(
            host=settings['MYSQL_HOST'],
            port=settings['MYSQL_PORT'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            db=settings['MYSQL_DBNAME'])
        conn = pymysql.connect(**db_config)
        return cls(conn)

    def process_item(self, item, spider):
        movie_name = item['movie_name']
        shorts = item['shorts']
        stars = item['stars']
        votes = item['votes']
        comment_time = item['comment_time']
        s = SnowNLP(shorts)
        sentiments = s.sentiments
        self.comment_list.append([movie_name, shorts, stars, votes, sentiments, comment_time])
        return item

    def close_spider(self, spider):
        insert_sql = 'INSERT INTO comments(`movie_name`,`shorts`,`stars`,`votes`,`sentiments`,`comment_time`) VALUES (%s,%s,%s,%s,%s,%s)'
        try:
            self.cursor.executemany(insert_sql, self.comment_list)
            self.conn.commit()
        except:
            self.conn.rollback()
        self.cursor.close()
        self.conn.close()
