# -*- coding: utf-8 -*-


import config as cfg
import MySQLdb
import datetime

# DAO
'''
Data Acess Object
실제로 data를 다루는 모듈을 dao라 함
save_neww(), get_news_by_id() 와 같이 인터페이스를 정의하여
데이터를 사용하는 쪽에서는 실제 db에 접근하는 코드를 최소화 함
'''

class NewsDAO(object):
    def __init__(self):
        self.db = MySQLdb.connect(cfg.DB_HOST, cfg.DB_USER, cfg.DB_PWD, cfg.DB_DB, use_unicode=True, charset="utf8")

    def save_news(self, news_id, title, topic, rel1, rel2, rel3, rel4, rel5, rel6, rel7):
        if not self.get_news_by_id(news_id):
            title = title.replace("'", '').replace('"', '')

            query = """INSERT INTO news
                    VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')""" \
                    .format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                    news_id, title, topic, rel1, rel2, rel3, rel4, rel5, rel6, rel7)

            cursor = self.db.cursor()
            try:
                cursor.execute(query)
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                print(e)
            finally:
                cursor.close()

    def get_news_by_id(self, news_id):
        query = "SELECT * FROM news WHERE url = '{}'".format(news_id)

        try:
            cursor = self.db.cursor()
            cursor.execute(query)

            row = cursor.fetchone()
            return row != None
        except Exception as e:
            print(e)
            return False
        finally:
            cursor.close()



    def close(self):
        try:
            self.db.close()
        except Exception as e:
            print(e)
