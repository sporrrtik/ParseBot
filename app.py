from flask import Flask, render_template, redirect, url_for, request, flash
from telegram_bot.sqlighter import SQLighter

# from collections import namedtuple
import datetime

app = Flask(__name__)
app.secret_key = 'some secret123'

# Message = namedtuple('Message', 'text tag')
# messages = []

# Connecting database
db = SQLighter('telegram_bot/db.db')


@app.route('/', methods=['GET', 'POST'])
def start():
    return render_template('sign_in.html')


@app.route('/main', methods=['GET'])
def main():
    login = request.args.get('login')
    return render_template('main.html', login=login)


@app.route('/sign_in', methods=['GET'])
def sign_in():
    return render_template('sign_in.html')


@app.route('/sign_up', methods=['GET'])
def sign_up():
    return render_template('sign_up.html')


@app.route('/admin_page', methods=['GET', 'POST'])
def admin_page():
    login = request.args.get('login')
    if login == 'sasha':
        return render_template('admin_page.html', user_list=db.get_all_users())
    flash("Do not try to cheat")
    return render_template('sign_in.html')


@app.route('/enter', methods=['POST'])
def enter():
    login = request.form['login']
    if db.data_is_correct(login, request.form['password']):
        if db.login_as_admin(login)[0][0]:
            return redirect(url_for('admin_page', login=login))
        return redirect(url_for('main', login=login))
    flash('Login or password is incorrect')
    return redirect(url_for('sign_in'))


@app.route('/unsub/<string:user_id>', methods=['GET', 'POST'])
def unsub(user_id):
    db.update_subscription(user_id, datetime.datetime.now(), False)
    return redirect(url_for('admin_page'))


@app.route("/ban/<string:user_id>", methods=['GET', 'POST'])
def ban(user_id):
    db.update_subscription(user_id, datetime.datetime.now(), False)
    db.ban_user(user_id=user_id, date=datetime.datetime.now())
    # print(db.user_is_banned(user_id, datetime.datetime.now()))
    return redirect(url_for('admin_page'))


@app.route('/register', methods=['POST'])
def register():
    if len(request.form['login']) == 0 or len(request.form['password']) == 0:
        flash('Please complete all fields')
    elif request.form['password'] == request.form['repeat-password']:
        if (not db.login_is_used(request.form['login'])):
            db.add_user(password=request.form['password'], login=request.form['login'])
            return redirect(url_for('sign_in'))
        else:
            flash('Your login is already gotten')
    else:
        flash('Your passwords are not the same')

    return redirect(url_for('sign_up'))



if __name__ == '__main__':
    app.run()
