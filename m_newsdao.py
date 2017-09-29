# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


import config as cfg
from pymongo import MongoClient



class M_NewsDAO(object):

    def __init__(self):
        self.db = MongoClient(cfg.mongo_DB_HOST, cfg.mongo_DB_PORT)


    def find_news(self, link):
        news = self.db.myarticles.articles
        try:
            found = news.find_one({'_id' : link})
            return found != None
        except Exception as e:
            print(e)
            return False
        finally:
            self.db.close()


    def save_news(self, link, title, content):
        news = self.db.myarticles.articles

        try:
            if not self.find_news(link):
                document = {}
                document['_id'] = link
                document['title'] = title
                document['content'] = content

                news.insert_one(document)
        except Exception as e:
            print(e)
        finally:
            self.db.close()

    def close(self):
        try:
            self.db.close()
        except Exception as e:
            print(e)