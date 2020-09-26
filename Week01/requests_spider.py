# 安装并使用 requests、bs4 库，爬取猫眼电影的前 10 个电影名称、电影类型和上映时间，并以 UTF-8 字符集保存到 csv 格式的文件中。

import requests
import random
from bs4 import BeautifulSoup as bs4
from fake_useragent import UserAgent

headers = {}

url = 'https://maoyan.com/films?showType=3'

# UA_LIST = [
#     # Windows Chrome
#     'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
#     # MAC Chrome
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
#     # Windows Firefox
#     'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
#     # MAC Firefox
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0',
#     # Safari
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'
# ]
# headers['User-Agent'] = random.choice(UA_LIST)

ua = UserAgent(verify_ssl=False)
headers['User-Agent'] = ua.random
headers['Cookie'] = 'uuid=33929200FC2311EA80FE9D7A0DEA9847193839B878A146A8AB40EB4D436373A6'

# 使用ip代理
ip_pool = ['http://104.129.196.194:8800']
ip = random.choice(ip_pool)
proxies = {'http:':ip}
resp = requests.get(url, headers=headers,proxies=proxies)

# resp = requests.get(url, headers=headers)
html = resp.text

movie_list = bs4(html, 'html.parser').find_all('div', attrs={'class': 'movie-hover-info'})

with open('maoyan_top10.csv', 'w', encoding='utf-8') as f:
    f.write('电影名称,电影类型,上映时间\n')
    # 前10个电影
    for movie_info in movie_list[:10]:
        name = movie_info.find('span', attrs={'class': 'name'}).text.strip()
        _type = movie_info.find_all('div', attrs={'class': 'movie-hover-title'}, limit=2)[-1].text.split(':')[
            -1].strip()
        release_time = movie_info.find('div', attrs={'class', 'movie-hover-brief'}).text.split(':')[-1].strip()
        f.write(f'{name},{_type},{release_time}\n')
