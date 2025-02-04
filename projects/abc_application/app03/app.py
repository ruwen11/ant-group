from flask import Flask
import psutil
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)

# Set up the PostgreSQL connection
def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        dbname=os.environ.get('DB_NAME', 'access_log'),
        user=os.environ.get('DB_USER', 'admin'),
        password=os.environ.get('DB_PASSWORD', 'password')
    )
    return conn

@app.route('/')
def hello_world():
    return "Hello World"

@app.route('/os-info')
def os_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    return f"CPU Usage: {cpu_usage}%"

@app.route('/log-access')
def log_access():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS access_log (id SERIAL PRIMARY KEY, timestamp TIMESTAMP, route VARCHAR(100));")
    cursor.execute("INSERT INTO access_log (timestamp, route) VALUES (%s, %s)", (datetime.now(), "/log-access"))
    conn.commit()

    cursor.execute("SELECT * FROM access_log;")
    logs = cursor.fetchall()

    conn.close()

    return f"Access logs:<br>{'<br>'.join([str(log) for log in logs])}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
