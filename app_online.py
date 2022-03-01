# -*- coding: utf-8 -*-

from flask import jsonify, Flask, request
from settings import conf
from src.weighted_tree import qa

app = Flask(__name__)
app.config.from_object(conf["test"])
app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"


@app.route('/qa/acvt', methods=['GET'])
def link_entity():
    sentence = request.args['sentence']
    ner = request.args['ner']
    result = qa.acvt_handle(sentence, ner)
    return jsonify(data={
        "code": 20000,
        "data": result
    })


@app.route('/qa/template', methods=['GET'])
def add_template():
    template = request.args
    print(template)
    data = []
    data.append(qa.add_template(template['question'], template['answer']))
    return {
        "code": 20000,
        "data": data
    }


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=8000, debug=True)
