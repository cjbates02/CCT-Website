from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import date


app = Flask(__name__)



def getDatabaseConnection():
    connection = sqlite3.connect('cct_database.db')
    connection.row_factory = sqlite3.Row
    return connection

@app.route('/delete_announcement', methods=['POST'])
def delete_announcement_api():
    id = request.get_json()
    id = id['delete_id']
    print(id)
    return jsonify(id=id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/announcements')
def announcements():
    conn = getDatabaseConnection()
    announcements = conn.execute('SELECT * FROM announcements').fetchall()
    conn.close()
        
    return render_template('announcements.html', annoucements=announcements[::-1])

@app.route('/new_announcement', methods=['GET', 'POST'])
def new_announcement():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        creator = request.form['creator']
        today_date = date.today()

        conn = getDatabaseConnection()
        conn.execute("INSERT INTO announcements (name, description, creator, date) VALUES (?,?,?,?)", (name, description, creator, today_date))
        conn.commit()
        conn.close()


        return redirect(url_for('announcements'))

    return render_template('new_announcement.html')


# @app.route('/delete_announcement')
# def delete_announcement():
#     conn = getDatabaseConnection()
#     announcements = conn.execute('SELECT * FROM announcements').fetchall()
#     conn.close()

#     return render_template('delete_announcement.html', announcements=announcements[::-1])

