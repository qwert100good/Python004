# -*- coding: utf-8 -*-
"""
@author : Yx
"""
import configparser
import threading
import time

import pymysql
from pymysql import OperationalError
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException

CITIES = {
    'beijing': '北京',
    'shanghai': '上海',
    'guangzhou': '广州',
    'shenzhen': '深圳'
}


class LaGouSpider(threading.Thread):
    def __init__(self, city):
        super().__init__()
        self.city = city
        self.count = 0
        self.job_info = []

    def init(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()

    def search(self, city):
        self.driver.get(f'https://www.lagou.com/{city}/')
        self.driver.find_element_by_css_selector('input.search_input').send_keys('Python 工程师')
        self.driver.find_element_by_id('search_button').click()
        # 弹出框
        self.driver.find_element_by_css_selector('div.body-btn').click()

    def spider(self):
        try:
            title_list = [title.text for title in self.driver.find_elements_by_tag_name('h3')]
            companies = [company.text for company in self.driver.find_elements_by_css_selector('div.company_name>a')]
            money = [self._get_avg_money(m.text) for m in self.driver.find_elements_by_css_selector('span.money')]
        except StaleElementReferenceException:
            time.sleep(1)
            title_list = [title.text for title in self.driver.find_elements_by_tag_name('h3')]
            companies = [company.text for company in self.driver.find_elements_by_css_selector('div.company_name>a')]
            money = [self._get_avg_money(m.text) for m in self.driver.find_elements_by_css_selector('span.money')]

        self.count += len(title_list)
        self.job_info.extend(zip(title_list, companies, money))

    def _get_avg_money(self, money):
        low, high = money.split('-')
        low_money = low.strip('k')
        high_money = high.strip('k')
        avg_money = (int(low_money) + int(high_money)) / 2
        return avg_money * 1000

    def next_page(self):
        self.driver.find_element_by_css_selector('div.next_disabled').click()

    def save_my_sql(self):
        if not self.job_info:
            return
        self.job_info = [[CITIES[self.city]] + list(info) for info in self.job_info]
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')
        mysql_config = {item[0]: eval(item[1]) for item in config.items('mysql')}
        try:
            conn = pymysql.connect(**mysql_config)
            cur = conn.cursor()
        except (OperationalError, Exception):
            print('数据库链接失败')
            return
        try:
            cur.executemany(
                'INSERT INTO job_info(`city`,`title`,`company`,`money`) VALUES (%s,%s,%s,%s)',
                self.job_info)
            conn.commit()
        except Exception:
            conn.rollback()
        finally:
            cur.close()
            conn.close()

    def run(self):
        self.init()
        self.search('beijing')
        self.spider()
        while self.count < 100:
            self.next_page()
            self.spider()
        time.sleep(10)
        self.save_my_sql()
        self.driver.close()


if __name__ == '__main__':
    city_list = ['beijing', 'shanghai', 'guangzhou', 'shenzhen']
    threads = []

    for city in city_list:
        spider_thread = LaGouSpider(city)
        threads.append(spider_thread)
        spider_thread.start()

    for t in threads:
        t.join()
