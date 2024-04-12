
import sqlite3

conn = sqlite3.connect('cct_database.db')
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS red_stack (
service_id integer primary key autoincrement,
name text,
ip text,
desc text,
username text,
password text
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS blue_stack (
service_id integer primary key autoincrement,
name text,
ip text,
desc text,
username text,
password text
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS purple_stack (
service_id integer primary key autoincrement,
name text,
ip text,
desc text,
username text,
password text
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS events (
event_id integer primary key autoincrement,
title text,
start date,
end date,
all_day integer
);
""")


# cur.execute("""
# INSERT INTO red_stack (name, ip , desc, username, password)
# VALUES ('vmware', '10.0.97.21', 'web server with apache2', 'root', 'PlattsburgH12901')
# """)

# cur.execute("""
# INSERT INTO blue_stack (name, ip , desc, username, password)
# VALUES ('splunk', '10.0.97.22', 'splunk enterprise', 'root', 'PlattsburgH12901')
# """)

# cur.execute("""
# INSERT INTO purple_stack (name, ip , desc, username, password)
# VALUES ('active directory', '10.0.97.23', 'account management', 'root', 'PlattsburgH12901')
# """)


cur.close()
conn.commit()
conn.close()