from app.algorithm import *
from flask import (
    Blueprint, flash, render_template, request
)

bp = Blueprint('search', __name__, url_prefix='/')


@bp.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')


@bp.route('/search', methods=('GET', 'POST'))
def search():

    query = request.form['keyword']

    return render_template('paper.html', result=algorithm('keyword', query), search_keyword = query)
