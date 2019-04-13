from flask import Flask, render_template, request, redirect, url_for, session
from flaskr.poem import nlp_result, parse_error, parse_couplets, parse_poem
import random

app = Flask(__name__)

token_key = '【获取的token】，参见 poem.py'


@app.route("/", methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        couplets = request.form.get('couplets')
        if couplets is not None:
            return redirect(url_for('get_couplets'))
        poem = request.form.get('poem')
        if poem is not None:
            return redirect(url_for('get_poem'))

    return render_template('couplets/index.html')


@app.route("/couplets", methods=('GET', 'POST'))
def get_couplets():
    if request.method == 'POST':
        center = None
        first = None
        second = None
        title = request.form.get('theme')
        back = request.form.get('back')
        if back == '返回':
            return redirect(url_for('index'))
        index = random.randint(0, 10)
        data = nlp_result(title, token_key, index, way='couplets')
        error = parse_error(data)
        if not error:
            center, first, second = parse_couplets(data)
        return render_template('couplets/show.html',
                               center=center,
                               first=first,
                               second=second,
                               title=title,
                               error=error)
    return render_template('couplets/base.html')


@app.route("/poem", methods=('GET', 'POST'))
def get_poem():
    if request.method == 'POST':
        title = None
        poem = None
        title = request.form.get('theme')
        back = request.form.get('back')
        if back == '返回':
            return redirect(url_for('index'))
        index = random.randint(0, 10)
        data = nlp_result(title, token_key, index, way='poem')
        error = parse_error(data)
        if not error:
            title, poem = parse_poem(data)
        return render_template('couplets/poem_show.html',
                               title=title,
                               poem=poem,
                               error=error)
    return render_template('couplets/poem_index.html')


if __name__ == '__main__':
    app.run(debug=True)
