# -*- coding: utf-8 -*-

from flask import jsonify, Flask, request, current_app
from src.cypher import Cypher
from utils.generate_poetry import generate_poetry
from src.mysql_manager import MysqlManager
from src.get_attr_and_relation import get_option_relation, predict_second_entity
from utils.mysql import OperationMysql
from settings import conf
from utils.user import getUserPoetryDetails
from src.weighted_tree import qa

app = Flask(__name__)
app.config.from_object(conf["test"])
app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"

from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("SIKU-BERT/sikubert")

model = AutoModel.from_pretrained("SIKU-BERT/sikubert")


# app.config.from_object(conf["pro"])
# bp = Blueprint("test", __name__, url_prefix='/')
# app.register_blueprint(bp, url_prefix='/')


@app.route('/entity', methods=['GET'])
def get_entity_id():
    entity_name = request.args.get('entity_name', '')
    entity_ner = request.args.get('entity_ner', '')
    data = Cypher.get_entity(entity_name, entity_ner)
    return {
        "code": 20000,
        "data": data
    }


@app.route('/poetry', methods=['GET'])
def get_poetry():
    text = generate_poetry()
    return {
        "code": 20000,
        "message": "成功",
        "data": text
    }


@app.route('/user/login', methods=['POST'])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    opera = OperationMysql()
    current_app.logger.info("{} --- {}".format(username, password))
    userinfo = opera.search_one(
        "select * from User where username = '{}'".format(username))
    current_app.logger.info(userinfo)
    if userinfo["password"] == password:
        result = {"code": 20000, "token": userinfo["id"]}
    else:
        result = {"code": 300}
    return result


@app.route('/user/logout', methods=['POST'])
def logout():
    return {"code": 20000}


@app.route('/poetry/entity_attr', methods=['GET'])
def poetry_attr():
    id_ = request.args.get("id")
    entity_list = get_option_relation(id_)
    return {
        "code": 20000,
        "message": "成功",
        "data": entity_list
    }


@app.route('/poetry/get_entity_value', methods=['GET'])
def poetry_entity_value():
    id_ = request.args.get("id")
    attr_name = request.args.get("attr")
    value = predict_second_entity(id_, attr_name)
    return {
        "code": 20000,
        "data": value
    }


@app.route('/user/info', methods=['GET'])
def userinfo():
    token = request.args.get("token")
    opera = OperationMysql()
    userinfo = opera.search_one(
        "select * from User where id = '{}'".format(token))

    return {
        "code": 20000,
        "data": {
            "roles": ['admin'],
            "introduction": 'I am a super administrator',
            "avatar": 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
            "name": userinfo["username"]
        }
    }


@app.route('/update/end_data', methods=['POST'])
def save_data_to_database():
    req = request.args
    current_app.logger.info(
        "{} --- {} --- {}".format(request.json, request.args, request.form))
    msg = MysqlManager.save_data(
        req['id'], (req['username']), (req['taged_data']))
    return {
        "code": 20000,
        "data": msg
    }


@app.route('/table/list', methods=['GET'])
def getTagsDetails():
    return {
        "code": 20000,
        "data": getUserPoetryDetails()
    }


@app.route('/qa/restart', methods=['GET'])
def init():
    current_app.logger.info("restart")
    data = qa.load_template()
    return {
        "code": 20000,
        "data": data
    }


# @app.route('/qa/template', methods=['POST'])
# def add_template():
#     template = request.json
#     print(template)
#     current_app.logger.info(template)
#     qa.add_question_to_db(template)
#     return {
#         "code": 20000,
#         "data": template
#     }

@app.route('/qa/template', methods=['GET'])
def add_template():
    template = request.args
    print(template)
    current_app.logger.info(template)
    data = []
    data.append(qa.add_template(template['question'], template['answer']))
    return {
        "code": 20000,
        "data": data
    }


# @app.route('/qa/test', methods=['POST'])
# def test_question():
#     one_question = request.json
#     ans = qa.online_qa(one_question)
#     return {
#         "code": 20000,
#         "data": ans
#     }

@app.route('/qa/test', methods=['GET'])
def test_question():
    one_question = request.args
    ans = qa.online_qa(one_question['question'])
    return {
        "code": 20000,
        "data": ans
    }


@app.route('/qa/entity/link', methods=['GET'])
def link_entity():
    sentence = request.args['sentence']
    print(sentence)
    result = qa.link_entity_ids(sentence)
    return {
        "code": 20000,
        "data": result
    }


@app.route('/qa/acvt', methods=['GET'])
def link_entity():
    print(request.json)
    sentence = request.args['sentence']
    ner = request.args['ner']
    result = qa.acvt_handle(sentence, ner)
    return jsonify(data={
        "code": 20000,
        "data": result
    })


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=8000, debug=True)
