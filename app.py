from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB bağlantı ayarları
client = MongoClient("mongodb://post_db:27017/")
db = client['post_service']
posts_collection = db['posts']

@app.route('/posts', methods=['GET'])
def get_posts():
    posts = posts_collection.find()
    return jsonify([{'id': str(post['_id']), 'title': post['title'], 'content': post['content']} for post in posts])

@app.route('/posts', methods=['POST'])
def create_post():
    data = request.json
    new_post = {
        'title': data['title'],
        'content': data['content']
    }
    result = posts_collection.insert_one(new_post)
    return jsonify({'id': str(result.inserted_id), 'title': new_post['title'], 'content': new_post['content']}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0')

