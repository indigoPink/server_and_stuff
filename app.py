from pymongo import MongoClient
import inspect  

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbjunction

@app.route('/', methods= ['GEt'])
def get_root():
    return 'Home'

@app.route('/room', methods= ['POST'])
def post_room():
    res = db.room.insert_one(request.json)
    return "200"

@app.route('/room/<room_code>', methods= ['GET'])
def get_room():
    res = db.room.find_one({'room_code':room_code}, {'_id':False})
    return res

@app.route('/user', methods= ['POST'])
def post_user():
    res = db.user.insert_one(request.json)
    return '200'

@app.route('/user/<email>', methods= ['PATCH'])
def patch_user(email):
    user = db.user.find_one_and_update({'email': email}, {'$set': {'status': "live"}})
    return '200'

@app.route('/idea', methods = ['POST'])
def post_idea():
    res = db.idea.insert_one(request.json)
    return '200'

@app.route('/idea/<room_code>', methods = ['GET'])
def get_idea(room_code):
    res = db.idea.find({'room_code': room_code},{'_id':False})
    return '200'

@app.route('/idea/<id>', methods= ['PATCH'])
def patch_idea(id):
    idea_before = db.idea.find({'_id': id})
    new_vote_count = idea_before['vote_count'] + 1
    db.idea.update_one({'_id': id }, { '$set': {'vote_count': new_vote_count}})
    return '200'


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
