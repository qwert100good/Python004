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
    def __init__(self, city, job='Python 工程师'):
        super().__init__()
        self.city = city
        self.count = 0
        self.job = job
        self.job_info = []
        self._money_lst = {}

    def init(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()

    def search(self):
        self.driver.get(f'https://www.lagou.com/{self.city}/')
        self.driver.find_element_by_css_selector('input.search_input').send_keys(self.job)
        self.driver.find_element_by_id('search_button').click()
        # 弹出框
        self.driver.find_element_by_css_selector('div.body-btn').click()

    def spider(self):
        try:
            title_list = [title.text for title in self.driver.find_elements_by_tag_name('h3')]
            companies = [company.text for company in self.driver.find_elements_by_css_selector('div.company_name>a')]
            money = [m.text for m in self.driver.find_elements_by_css_selector('span.money')]
        except StaleElementReferenceException:
            time.sleep(1)
            title_list = [title.text for title in self.driver.find_elements_by_tag_name('h3')]
            companies = [company.text for company in self.driver.find_elements_by_css_selector('div.company_name>a')]
            money = [m.text for m in self.driver.find_elements_by_css_selector('span.money')]

        job_list = [Job(*params) for params in list(zip(title_list, companies, money))]
        # 去重
        for job in job_list:
            if self.count == 100:
                break
            self._money_lst[job.money] = 1
            self.job_info.append(job.info)
            self.count += 1

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
        self.search()
        self.spider()
        while self.count < 100:
            self.next_page()
            self.spider()
        self.save_my_sql()
        print(self.job_info)
        self.driver.close()


class Job:
    def __init__(self, title, company, money):
        self.title = title
        self.company = company
        self._money = money

    @property
    def money(self):
        low, high = self._money.split('-')
        low_money = low.strip('k')
        high_money = high.strip('k')
        avg_money = (int(low_money) + int(high_money)) / 2
        return avg_money * 1000

    @property
    def info(self):
        return self.title, self.company, self.money


if __name__ == '__main__':
    city_list = ['beijing', 'shanghai', 'guangzhou', 'shenzhen']
    threads = []

    for city in city_list:
        spider_thread = LaGouSpider(city, 'Python 工程师')
        threads.append(spider_thread)
        spider_thread.start()

    for t in threads:
        t.join()
