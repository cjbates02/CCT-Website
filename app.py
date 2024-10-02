from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import date

#start 
app = Flask(__name__)



def getDatabaseConnection():
    connection = sqlite3.connect('cct_database.db')
    connection.row_factory = sqlite3.Row
    return connection


@app.route('/view_service_info')
def view_service_info(service):
    return render_template('service_info.html', service=service)

@app.route('/add_event_form', methods=['GET', 'POST'])
def add_event_form():
    if request.method == 'POST':
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        start_time = request.form['start-time']
        end_time = request.form['end-time']
       

        if 'allday' in request.form:
            allday = request.form['allday']
            if allday == 'on':
                allday = 1
        else:
            allday = 0

        conn = getDatabaseConnection()
        conn.execute("""
        INSERT INTO EVENTS
        (title, start, end, all_day, start_time, end_time)
        VALUES (?,?,?,?,?,?)
        """, (title, start, end, allday, start_time, end_time))

        conn.commit()
        conn.close()
        return redirect(url_for('calendar'))

    return render_template('add_event.html')

@app.route('/delete_event', methods=['GET', 'POST'])
def delete_event():
    id = request.get_json()
    id = id['id']
    print(id)

    conn = getDatabaseConnection()
    conn.execute("DELETE FROM events WHERE event_id=?", (id,))
    conn.commit()
    conn.close()
    

@app.route('/calendar')
def calendar():
    conn = getDatabaseConnection()
    events = conn.execute("SELECT * FROM events")
    return render_template('calendar.html', events=events)



@app.route('/doc', methods=['GET', 'POST'])
def doc():
    if request.method == 'POST':
        data = request.form['service_data']
        data = data.split(',')
        id = data[0]
        stack = data[1]

        print(id, stack)

        conn = getDatabaseConnection()
        service = conn.execute(f"SELECT * FROM {stack} WHERE service_id = ?", (id,)).fetchone()
        conn.close()
        return view_service_info(service)


    conn = getDatabaseConnection()

    blue_stack_data = conn.execute("SELECT * FROM blue_stack").fetchall()
    red_stack_data = conn.execute("SELECT * FROM red_stack").fetchall()
    purple_stack_data = conn.execute("SELECT * FROM purple_stack").fetchall()

    print(blue_stack_data)

    return render_template('doc.html', blue_stack_data=blue_stack_data, purple_stack_data=purple_stack_data, red_stack_data=red_stack_data)

@app.route('/add_service', methods=['GET', 'POST'])
def add_service():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        ip = request.form['ip']
        desc = request.form['desc']
        username = request.form['username']
        stack = request.form.get('network-stack')
        print(stack)
        conn = getDatabaseConnection()
        conn.execute(f'INSERT INTO {stack} (name, ip, desc, username, password) VALUES (?, ?, ?, ?, ?)', (name, ip, desc, username, password))
        conn.commit()
        conn.close()

        return redirect(url_for('doc'))

    return render_template('add_service.html')

@app.route('/delete_announcement', methods=['GET', 'POST'])
def delete_announcement_api():
    id = request.get_json()
    id = id['id']

    conn = getDatabaseConnection()
    conn.execute("DELETE FROM announcements WHERE id=?", (id,))
    conn.commit()
    conn.close()


@app.route('/delete_doc', methods=['GET', 'POST'])
def delete_doc_api():
    data = request.get_json()
    id = data['id']
    stack = data['stack']

    conn = getDatabaseConnection()
    conn.execute(f"DELETE FROM {stack} WHERE service_id=?", (id,))
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
    conn = getDatabaseConnection()
    
    announcements = conn.execute('SELECT * FROM announcements').fetchall()
    changes = conn.execute('SELECT * FROM change_log').fetchall()
    
    return render_template('index.html', announcements=announcements, changes=changes)


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

