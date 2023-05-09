from flask import Flask, render_template, request, redirect, session
import bcrypt
import os
import psycopg2

#db journal_db

app = Flask(__name__)

@app.route('/')
def index():
    # connection = psycopg2.connect(host=os.getenv("PGHOST"), user=os.getenv("PGUSER"), password=os.getenv("PGPASSWORD"), port=os.getenv("PGPORT"), dbname=os.getenv("PGDATABASE"))
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM mytable;")
    results = cursor.fetchall()
    connection.close()
    return f"{results[0]}"

@app.route('/entries')
def entries():
    connection = psycopg2.connect("dbname=journal_db", port=5433, password="3113")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM journal_entries;")

    entries = cursor.fetchall()
    connection.close()
    return render_template("entries.html", entries=entries)

@app.route('/forms/entries/add')
def add_entry_form():
    return render_template('add_entry.html')

@app.route('/api/entries/add', methods=['POST'])
def add_entry():
    title = request.form['title']
    content = request.form['content']
    # user_id = session['user_id']

    # Connect to the database and insert the new entry
    connection = psycopg2.connect("dbname=journal_db", port=5433, password="3113")

    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO journal_entries (title, content) VALUES (%s, %s)",
        [title, content]
    )
    connection.commit()
    connection.close()

    return redirect('/entries')


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))

#button new note, onlick, second screen. 
#simple form, input heading for form 
#/chat route 
# text box towards the end/botton of screen. 
#user types in text box, presses sends. sends to flask app, aand then forward that input to chagpt, chatgpt sends you response, 
#users tab;e, notes table, message table, key table.
#how do you identify that a given record a reply, or original message was sent, how will you figure out the sequence of messages. 