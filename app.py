from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from threading import Thread
import os
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Users(db.Model):
    id_ = db.Column("id_", db.Integer, primary_key=True)
    email = db.Column("email", db.String(50))
    expiration_datetime = db.Column('expiration_datetime', db.DateTime())

    def __init__(self, email, expiration_datetime):
        self.email = email
        self.expiration_datetime = expiration_datetime


def threaded_task():
    while True:
        conn = sqlite3.connect(os.environ.get('DATABASE_URL_DIRECT'), check_same_thread=False)
        cursor = conn.cursor()
        sql = "DELETE FROM users WHERE expiration_datetime < datetime('now')"
        cursor.execute(sql)
        conn.commit()
        conn.close()


@app.before_first_request
def create_table_and_start_thread():
    db.create_all()
    thread = Thread(target=threaded_task)
    thread.daemon = True
    thread.start()


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        email_received = request.form["em"]
        found_email = Users.query.filter_by(email=email_received).first()

        if found_email:
            return render_template("home.html", reply=f"Вже бачилися, {email_received}")

        else:
            expiration_datetime = datetime.now() + timedelta(hours=1)
            new_email = Users(email_received, expiration_datetime)
            db.session.add(new_email)
            db.session.commit()
            return render_template("home.html", reply=f"Привіт, {email_received}")

    else:
        return render_template("home.html")


@app.route('/all_emails')
def display_all():
    return render_template('all_users.html', users=Users.query.all())


if __name__ == '__main__':
    port = os.environ.get("PORT", 5000)
    app.run(debug=False, host='0.0.0.0', port=port)
