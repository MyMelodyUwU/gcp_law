import logging
import sqlite3
from flask import Flask, request

logging.basicConfig(filename='database_changes.log', level=logging.INFO, format='%(asctime)s - %(message)s')

logging.basicConfig(filename='webserver_requests.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

def log_change(action, details):
    logging.info(f"{action} - {details}")

def log_request_info():
    logging.info(f"Request from {request.remote_addr} to {request.url} with method {request.method}")

def insert_into_db(name,filling,sauce,extras):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO burrito (name, filling, sauce, extras) VALUES (?,?,?,?)", (name,filling,sauce,extras))
    conn.commit()
    conn.close()
    log_change("INSERT", f"name: {name}, filling: {filling}, sauce: {sauce}, extras: {extras}")


@app.route('/add', methods=['POST'])
def add_entry():
        log_request_info()
        name = request.form['name']
        filling = request.form['filling']
        sauce = request.form['sauce']
        extras = request.form['extras']
        insert_into_db(name,filling,sauce,extras)
        return f"Added {name,filling,sauce,extras} to the database!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
