from flask import Flask, render_template, redirect, url_for, request, flash
from telegram_bot.sqlighter import SQLighter

from collections import namedtuple

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'some secret123'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# db = SQLAlchemy(app)


Message = namedtuple('Message', 'text tag')
messages = []


# Connecting database
db = SQLighter('telegram_bot/db.db')


@app.route('/', methods=['GET','POST'])
def hello_world():
    return render_template('index.html')


@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html', messages=messages)


@app.route('/sign_in', methods=['GET'])
def sign_in():
    return render_template('sign_in.html')


@app.route('/sign_up', methods=['GET'])
def sign_up():
    return render_template('sign_up.html')


@app.route('/add_message', methods=['POST'])
def add_message():
    text = request.form['text']
    tag = request.form['tag']

    messages.append(Message(text, tag))

    return redirect(url_for('main'))


@app.route('/register', methods=['POST'])
def register():
    if request.form['password'] == request.form['repeat-password']:
        if not (db.login_is_used(request.form['login'])):
            db.add_user(password=request.form['password'], login=request.form['login'])
            return render_template('index.html')
        else:
            flash('Your login is already gotten')
    else:
        flash('Your passwords are not the same')

    return redirect(url_for('sign_up'))


@app.route('/enter', methods=['POST'])
def enter():
    if db.data_is_correct(request.form['login'], request.form['password']):
        return render_template('index.html')
    flash('Login or password is incorrect')
    return redirect(url_for('sign_in'))



if __name__ == '__main__':
    app.run()
