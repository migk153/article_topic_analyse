# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


import requests
from bs4 import BeautifulSoup
from m_newsdao import M_NewsDAO


def find_a(tags):
    return tags.name == 'a' and not tags.has_attr('class') and tags.has_attr('href')

class NaverNewsCrawler(object):

    def __init__(self, newsdao, urls):
        self.newsdao = newsdao
        self.urls = urls

    def crawl_link(self):
        for url in self.urls:
            res = requests.get(url)
            content = res.content

            soup = BeautifulSoup(content, 'html5lib')

            table = soup.find('table', attrs = {'class' : 'container'})
            for a in table.find_all(find_a):
                link = a['href']

                try:
                    self.crawl_title_content(link)
                except Exception as e:
                    continue

    def crawl_title_content(self, link):
        try:
            print (link)
            res = requests.get(link)
        except Exception as e:
            raise Exception('crawl error')

        content = res.text
        soup = BeautifulSoup(content, 'html5lib')

        # soup 에서 javascript 제거
        for script in soup(["script", "style"]):
            script.extract()

        # title 추출
        title = soup.find('h3', attrs = {'id' : 'articleTitle'})
        if title == None or title == '':
            return
        title = title.text

        # 본문 추출
        content = soup.find('div', attrs = {'id' : 'articleBodyContents'})
        if content == None or content == '':
            return
        content = content.text.strip()

        print (link)
        print (title)
        print



        try:
            self.newsdao.save_news(link, title, content)
        except Exception as e:
            print(e)


# 네이버 기사중 IT/과학 카테고리만 크롤링
urls = ['http://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=105']

import datetime
s = datetime.datetime.now()
print(s)

m_newsdao = M_NewsDAO()
crawler = NaverNewsCrawler(m_newsdao, urls)
crawler.crawl_link()

m_newsdao.close()

e = datetime.datetime.now()
print('start time: ',s)
print('end time:',e)
