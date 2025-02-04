# version2.py
import psutil
from flask import Flask
app = Flask(__name__)

@app.route('/')
def os_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    return f'CPU Usage: {cpu_usage}%'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
