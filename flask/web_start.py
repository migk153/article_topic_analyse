# -*- coding: utf-8 -*-

import config as cfg
import MySQLdb
from flask import Flask, jsonify, render_template, request

# flask 객체 생성
app = Flask(__name__)

# plain text 반환
@app.route('/ta')
def initiate_page():
    return render_template('home.html')

@app.route('/recommend_article', methods=['POST'])
def recommend_article():
    topic_to_find = request.form['topic']
    try:
        db = MySQLdb.connect(cfg.DB_HOST, cfg.DB_USER, cfg.DB_PWD, cfg.DB_DB, use_unicode=True, charset="utf8")
        cursor = db.cursor()

        query = """select title, url from news where topic like '%{}%' """.format(topic_to_find)
        # 쿼리를 문자열로 전닯
        cursor.execute(query)
        # 한개만 가져옴
        temp_data = cursor.fetchall()
        data = []
        for i in range(len(temp_data)):
            #if len(temp_data[i]) == 2:
            data.append({'title':temp_data[i][0], 'url':temp_data[i][1]})
    except Exception as e:
        return str(e)
    finally:
        # 연결 종료
        db.close()
    return render_template('recommend_page.html',
                            articles = data,
                            topic = topic_to_find)

app.run(host='0.0.0.0', port=5001, debug=True)
