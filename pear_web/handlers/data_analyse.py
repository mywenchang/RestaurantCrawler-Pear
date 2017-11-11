# coding=utf-8
from pear_web import app
from flask.app import request


@app.route('/analyse', methods=['GET', 'POST'])
@app.route('/analyse/<int:analyse_id>', methods=['GET', 'POST'])
def analyse(analyse_id=None):
    if request.method == 'GET':
        return 'get'
    elif request.method == 'POST':
        return 'post'
    return 'analyse'
