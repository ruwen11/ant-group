from flask import Flask, render_template, request
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)

# Database connection parameters
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'access_logs')
DB_USER = os.environ.get('DB_USER', 'user')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')

# Connect to PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

# Create table if it doesn't exist
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS access_logs (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            user_agent TEXT
        );
    ''')
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/')
def index():
    # Log the access with user-agent and timestamp
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO access_logs (timestamp, user_agent) VALUES (%s, %s)",
        (datetime.now(), request.headers.get('User-Agent'))
    )
    conn.commit()

    # Fetch the latest access logs to display on the website
    cursor.execute("SELECT * FROM access_logs ORDER BY timestamp DESC;")
    logs = cursor.fetchall()  # Get all rows

    cursor.close()
    conn.close()
    
    # Pass the logs to the template to display them
    return render_template('index.html', logs=logs)

if __name__ == '__main__':
    create_table()
    app.run(host='0.0.0.0', port=5000)
