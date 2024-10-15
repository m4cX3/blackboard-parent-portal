from flask import Flask, render_template, request, g
import sqlite3

app = Flask(__name__)
DATABASE = 'mydatabase.db'

# Database connection function
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Close connection when app context ends
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Route to display data
@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM my_table")  # Example query
    rows = cursor.fetchall()
    return render_template('index.html', rows=rows)

# Sample route to insert data
@app.route('/add', methods=['POST'])
def add_data():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO my_table (column1) VALUES (?)", (request.form['value'],))
    db.commit()
    return 'Data added!'

if __name__ == '__main__':
    app.run(debug=True)
