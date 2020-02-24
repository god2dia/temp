from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/test', methods=['GET'])
def test_get():
    # rank_give로 클라이언트가 준 rank을 가져오기
    recipe_title_receive = request.args.get('recipe_title_give')

    # rank의 값이 받은 rank와 일치하는 document 찾기 & _id 값은 출력에서 제외하기{$regex:"sd"})
    title_info = list(db.soomis_official_recipes.find({'title':{'$regex':recipe_title_receive}}, {'_id': 0}))
    # recipe_info = list(db.paik_recipes.find({'title': {'$regex': title_receive}}, {'_id': 0}))
    # info라는 키 값으로 타이틀 내려주기
    return jsonify({'result': 'success', 'info': title_info})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

    # ///////////////test//////////////////////
#     검색시 이렇게 검색 하세요
# 56000/test?=recipe_title_give=노가리볶음
