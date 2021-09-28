from flask import Flask, jsonify, request
import csv

from storage import all_articles, liked_articles, not_liked_articles
from demographic_filtering import output
from content_filtering import get_recommendations

all_articles = []

with open('articles.csv')as f:
    reader = csv.reader(f)
    data = list(reader)
    all_articles = data[1:]

liked_articles = []
not_liked_articles = []

app = Flask(__name__)

@app.route('/get-article')
def get_article():
    return jsonify({
        'data': all_articles[0],
        'status':'success'
    })

@app.route('/liked-article', methods = ['POST'])
def liked_article():
    article = all_articles[0]
    liked_article.append(article)
    all_articles.pop(0)
    return jsonify({
        'status':'success'
    }),201

@app.route('/not-liked-article', methods = ['POST'])
def not_liked_article():
    article = all_articles[0]
    not_liked_article.append(article)
    all_articles.pop(0)
    return jsonify({
        'status':'success'
    }),201

@app.route("/popular-articles")
def popular_articles():
    articles_data = []
    for articles in output:
        _d = {
            "url": articles[0],
            "title": articles[1],
            "text": articles[2],
            "lan": articles[3],
            "total_events": articles[4]
        }
        articles_data.append(_d)
    return jsonify({
        "data": articles_data,
        "status": "success"
    }), 200

@app.route("/recommended-articles")
def recommended_articles():
    all_recommended = []
    for liked_article in liked_articles:
        output = get_recommendations(liked_article[4])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    article_data = []
    for recommended in all_recommended:
        _d = {
            "url": recommended[0],
            "title": recommended[1],
            "text": recommended[2],
            "lan": recommended[3],
            "total_events": recommended[4]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200

if __name__ == "__main__":
    app.run()

