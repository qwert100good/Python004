# V1.0
# 安装并使用 requests、bs4 库，爬取猫眼电影的前 10 个电影名称、电影类型和上映时间，并以 UTF-8 字符集保存到 csv 格式的文件中。
# V2.0
# 将保存至 csv 文件的功能修改为保持到 MySQL，并在下载部分增加异常捕获和处理机制。

import requests
import random
import datetime
import pymysql
import configparser
from bs4 import BeautifulSoup as bs4
from fake_useragent import UserAgent
from pymysql import OperationalError


def get_movie_info():
    headers = {}
    movie_info_list = []
    url = 'https://maoyan.com/films?showType=3'
    ua = UserAgent(verify_ssl=False)
    headers['User-Agent'] = ua.random
    headers['Cookie'] = 'uuid=33929200FC2311EA80FE9D7A0DEA9847193839B878A146A8AB40EB4D436373A6'

    # 使用ip代理
    ip_pool = [
        'http://180.97.33.212:80',
        'http://180.97.33.144:80',
        'http://180.97.104.97:80',
        'http://180.149.144.224:80',
        'http://180.149.144.176:80'
    ]
    ip = random.choice(ip_pool)
    proxies = {'http:': ip}
    try:
        resp = requests.get(url, headers=headers, proxies=proxies)
        html = resp.text
        movie_list = bs4(html, 'html.parser').find_all('div', attrs={'class': 'movie-hover-info'})
    except Exception:
        print('获取网页源码失败')
    else:
        for movie_info in movie_list[:10]:
            name = movie_info.find('span', attrs={'class': 'name'}).text.strip()
            _type = movie_info.find_all('div', attrs={'class': 'movie-hover-title'}, limit=2)[-1].text.split(':')[
                -1].strip()
            release_time = movie_info.find('div', attrs={'class', 'movie-hover-brief'}).text.split(':')[-1].strip()
            movie_info_list.append(f'{name},{_type},{release_time}\n')
    return movie_info_list


def save_csv(movie_info):
    if not movie_info:
        return
    with open('maoyan_top10.csv', 'w', encoding='utf-8') as f:
        f.write('电影名称,电影类型,上映时间\n')
        # 前10个电影
        f.writelines(movie_info)


def save_mysql(movie_info):
    if not movie_info:
        return
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    mysql_config = {item[0]: eval(item[1]) for item in config.items('mysql')}
    try:
        conn = pymysql.connect(**mysql_config)
        cur = conn.cursor()
    except (OperationalError, Exception):
        print('数据库链接失败')
        return
    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    movie_info_list = [tuple(row.strip().split(',') + [create_time]) for row in movie_info]
    try:
        cur.executemany('INSERT INTO movie_info(`name`,`type`,`release_time`,`create_time`) VALUES (%s,%s,%s,%s)',
                        movie_info_list)
        conn.commit()
    except Exception:
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def main():
    movie_info = get_movie_info()
    # save_csv(movie_info)
    save_mysql(movie_info)


if __name__ == '__main__':
    main()
