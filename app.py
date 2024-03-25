from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import date


app = Flask(__name__)



def getDatabaseConnection():
    connection = sqlite3.connect('cct_database.db')
    connection.row_factory = sqlite3.Row
    return connection



@app.route('/doc')
def doc():
    return render_template('doc.html')

@app.route('/delete_announcement', methods=['GET', 'POST'])
def delete_announcement_api():
    id = request.get_json()
    id = id['id']

    conn = getDatabaseConnection()
    conn.execute("DELETE FROM announcements WHERE id=?", (id,))
    conn.commit()
    conn.close()

@app.route('/delete_change_log', methods=['GET', 'POST'])
def delete_change_log_api():
    id = request.get_json()
    id = id['id']

    conn = getDatabaseConnection()
    conn.execute("DELETE FROM change_log WHERE id=?", (id,))
    conn.commit()
    conn.close()




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/change_log', methods=['GET', 'POST'])
def change_log():
    if request.method == 'POST':
        id = request.form['change_id']
        conn = getDatabaseConnection()
        change_log = conn.execute("SELECT * FROM change_log WHERE id = ?", (id,)).fetchone()
        conn.close()
        return change_card(change_log)

    conn = getDatabaseConnection()
    changes = conn.execute('SELECT * FROM change_log').fetchall()
    conn.close()

    return render_template('change_log.html', changes=changes)



@app.route('/new_change_log', methods=['GET', 'POST'])
def new_change_log():
    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']
        creator = request.form['creator']
        rollback_steps = request.form['rollback_steps']
        todays_date = date.today()

        conn = getDatabaseConnection()
        conn.execute("INSERT INTO change_log (name, rollback_steps, creator, date, description) VALUES (?,?,?,?,?)", (name, rollback_steps, creator, todays_date, description))
        conn.commit()
        conn.close()

        return redirect(url_for('change_log'))


    return render_template('new_change_log.html')


@app.route('/change_card')
def change_card(change_card):
    return render_template('change_card.html', change_card=change_card)


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

