from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


# @app.route('/test', methods=['GET'])
@app.route('/s_follow_recipe', methods=['GET'])
def listing():
    soomi_follow_recipe = list(db.soomis_follow_recipes.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'soomis_follow': soomi_follow_recipe})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)