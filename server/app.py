#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate
from sqlalchemy import DateTime, func
from datetime import datetime
from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    session.clear()
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():

    pass

@app.route('/articles/<int:id>', methods=['GET'])
def show_article(id):
    session['page_views'] = session.get('page_views', 0)
    session['page_views'] += 1
    if session['page_views'] <= 3:
        article_data = {
            'article_id': id,
            'content': f'Article content for id {id}',
            'author': 'John Doe',
            'title': f'Title for article {id}',
            'preview': f'Preview for article {id}',
            'minutes_to_read': 5,
            'date': datetime.now().isoformat()
        }
        return jsonify(article_data), 200
    else:
        error_message = {'message': 'Maximum pageview limit reached'}
        return jsonify(error_message), 401

if __name__ == '__main__':
    app.run(port=5555)