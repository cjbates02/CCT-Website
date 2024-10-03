
from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3  # For database connection
from datetime import date

# Initialize Flask application
app = Flask(__name__)

# Function to establish a connection with the SQLite database
def getDatabaseConnection():
    connection = sqlite3.connect('cct_database.db')  # Connect to database
    connection.row_factory = sqlite3.Row  # To access columns by name
    return connection  # Return the connection object

# Route to view service information based on the provided service data
@app.route('/view_service_info')
def view_service_info(service):
    return render_template('service_info.html', service=service)

# Route to add an event through a form, supports GET and POST requests
@app.route('/add_event_form', methods=['GET', 'POST'])
def add_event_form():
    if request.method == 'POST':  # Handle form submission
        # Collect event details from the form
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        start_time = request.form['start-time']
        end_time = request.form['end-time']
       
        # Check if the event is all-day
        if 'allday' in request.form:
            allday = request.form['allday']
            if allday == 'on':
                allday = 1  # Mark as all-day event
        else:
            allday = 0  # Not an all-day event

        # Insert the new event into the database
        conn = getDatabaseConnection()
        conn.execute("""
        INSERT INTO EVENTS
        (title, start, end, all_day, start_time, end_time)
        VALUES (?,?,?,?,?,?)
        """, (title, start, end, allday, start_time, end_time))
        conn.commit()
        conn.close()

        # Redirect to the calendar page after insertion
        return redirect(url_for('calendar'))

    # Render the event form if the request is GET
    return render_template('add_event.html')

# Route to delete an event
@app.route('/delete_event', methods=['GET', 'POST'])
def delete_event():
    id = request.get_json()  # Get the event ID from the JSON request
    id = id['id']
    print(id)

    # Execute deletion of the event from the database
    conn = getDatabaseConnection()
    conn.execute("DELETE FROM events WHERE event_id=?", (id,))
    conn.commit()
    conn.close()

# Route to display the calendar with events
@app.route('/calendar')
def calendar():
    conn = getDatabaseConnection()
    events = conn.execute("SELECT * FROM events")  # Fetch all events
    return render_template('calendar.html', events=events)

# Route to view service details through a form
@app.route('/doc', methods=['GET', 'POST'])
def doc():
    if request.method == 'POST':
        # Retrieve service data from the form submission
        data = request.form['service_data']
        data = data.split(',')
        id = data[0]
        stack = data[1]

        print(id, stack)

        # Fetch service details from the selected stack
        conn = getDatabaseConnection()
        service = conn.execute(f"SELECT * FROM {stack} WHERE service_id = ?", (id,)).fetchone()
        conn.close()

        # Display the service information
        return view_service_info(service)

    # Fetch all stack data for display
    conn = getDatabaseConnection()
    blue_stack_data = conn.execute("SELECT * FROM blue_stack").fetchall()
    red_stack_data = conn.execute("SELECT * FROM red_stack").fetchall()
    purple_stack_data = conn.execute("SELECT * FROM purple_stack").fetchall()
    print(blue_stack_data)

    # Render the 'doc' page with the stack data
    return render_template('doc.html', blue_stack_data=blue_stack_data, purple_stack_data=purple_stack_data, red_stack_data=red_stack_data)

# Route to add a new service, supports GET and POST
@app.route('/add_service', methods=['GET', 'POST'])
def add_service():
    if request.method == 'POST':
        # Collect service details from the form
        name = request.form['name']
        password = request.form['password']
        ip = request.form['ip']
        desc = request.form['desc']
        username = request.form['username']
        stack = request.form.get('network-stack')
        print(stack)

        # Insert the new service into the selected stack
        conn = getDatabaseConnection()
        conn.execute(f'INSERT INTO {stack} (name, ip, desc, username, password) VALUES (?, ?, ?, ?, ?)', (name, ip, desc, username, password))
        conn.commit()
        conn.close()

        # Redirect to the 'doc' page after insertion
        return redirect(url_for('doc'))

    # Render the form to add a new service
    return render_template('add_service.html')

# Route to delete an announcement via API
@app.route('/delete_announcement', methods=['GET', 'POST'])
def delete_announcement_api():
    id = request.get_json()  # Get announcement ID from the JSON request
    id = id['id']

    # Delete the announcement from the database
    conn = getDatabaseConnection()
    conn.execute("DELETE FROM announcements WHERE id=?", (id,))
    conn.commit()
    conn.close()

# Route to delete service documentation
@app.route('/delete_doc', methods=['GET', 'POST'])
def delete_doc_api():
    data = request.get_json()  # Get service ID and stack name from JSON
    id = data['id']
    stack = data['stack']

    # Delete the service from the selected stack
    conn = getDatabaseConnection()
    conn.execute(f"DELETE FROM {stack} WHERE service_id=?", (id,))
    conn.commit()
    conn.close()

# Route to delete a change log entry
@app.route('/delete_change_log', methods=['GET', 'POST'])
def delete_change_log_api():
    id = request.get_json()  # Get change log ID from the JSON request
    id = id['id']

    # Delete the change log entry from the database
    conn = getDatabaseConnection()
    conn.execute("DELETE FROM change_log WHERE id=?", (id,))
    conn.commit()
    conn.close()

# Home route to display announcements and changes
@app.route('/')
def index():
    conn = getDatabaseConnection()

    # Fetch announcements and change logs
    announcements = conn.execute('SELECT * FROM announcements').fetchall()
    changes = conn.execute('SELECT * FROM change_log').fetchall()
    
    # Render the homepage with the fetched data
    return render_template('index.html', announcements=announcements, changes=changes)

# Route to display change log details
@app.route('/change_log', methods=['GET', 'POST'])
def change_log():
    if request.method == 'POST':
        id = request.form['change_id']  # Get change log ID from the form
        conn = getDatabaseConnection()
        change_log = conn.execute("SELECT * FROM change_log WHERE id = ?", (id,)).fetchone()
        conn.close()
        return change_card(change_log)

    # Fetch all change log entries
    conn = getDatabaseConnection()
    changes = conn.execute('SELECT * FROM change_log').fetchall()
    conn.close()

    # Render the change log page
    return render_template('change_log.html', changes=changes)

# Route to add a new change log entry
@app.route('/new_change_log', methods=['GET', 'POST'])
def new_change_log():
    if request.method == "POST":
        # Collect change log details from the form
        name = request.form['name']
        description = request.form['description']
        creator = request.form['creator']
        rollback_steps = request.form['rollback_steps']
        todays_date = date.today()  # Get the current date

        # Insert new change log into the database
        conn = getDatabaseConnection()
        conn.execute("INSERT INTO change_log (name, rollback_steps, creator, date, description) VALUES (?,?,?,?,?)", (name, rollback_steps, creator, todays_date, description))
        conn.commit()
        conn.close()

        # Redirect to the change log page after insertion
        return redirect(url_for('change_log'))

    # Render the form to create a new change log entry
    return render_template('new_change_log.html')

# Route to display a specific change log card
@app.route('/change_card')
def change_card(change_card):
    return render_template('change_card.html', change_card=change_card)

# Route to display all announcements
@app.route('/announcements')
def announcements():
    conn = getDatabaseConnection()

    # Fetch all announcements
    announcements = conn.execute('SELECT * FROM announcements').fetchall()
    conn.close()
    
    # Render the announcements page, reversing the order
    return render_template('announcements.html', announcements=announcements[::-1])

# Route to create a new announcement
@app.route('/new_announcement', methods=['GET', 'POST'])
def new_announcement():
    if request.method == 'POST':
        # Collect announcement details from the form
        name = request.form['name']
        description = request.form['description']
        creator = request.form['creator']
        today_date = date.today()  # Get the current date

        # Insert new announcement into the database
        conn = getDatabaseConnection()
        conn.execute("INSERT INTO announcements (name, description, creator, date) VALUES (?,?,?,?)", (name, description, creator, today_date))
        conn.commit()
        conn.close()

        # Redirect to the announcements page
        return redirect(url_for('announcements'))

    # Render the form to create a new announcement
    return render_template('new_announcement.html')

# Additional route (commented out) to delete an announcement manually
# @app.route('/delete_announcement')
# def delete_announcement():
#     conn = getDatabaseConnection()
#     announcements = conn.execute('SELECT * FROM announcements').fetchall()
#     conn.close()

#     return render_template('delete_announcement.html', announcements=announcements[::-1])