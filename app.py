from flask import Flask, render_template, request, redirect, session, jsonify
# from chatbot import chatbot_response
from models import common, user
from sentiment_analysis import gpt_classify_sentiment, emotions
import os
import openai
import bcrypt
import psycopg2


app = Flask(__name__)
app.config['SECRET_KEY'] = 'My secret key'
openai.api_key = open('key.txt').read().strip('\n')

@app.route('/')
def index():
    connection = psycopg2.connect(
        host=os.getenv("PGHOST"), 
        user=os.getenv("JUSER"), 
        password=os.getenv("PGPASSWORD"), 
        port=os.getenv("PGPORT"), 
        dbname=os.getenv("PGDATABASE"))
    # connection = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM mytable;")
    results = cursor.fetchall()
    connection.close()
    return f"{results[0]}"

@app.route('/entries')
def entries():
    if not session.get("user_id", ""):
        return redirect("/login")

    user_id = session["user_id"]
    connection = psycopg2.connect(host=os.getenv("PGHOST"), user=os.getenv("JUSER"), password=os.getenv("PGPASSWORD"), port=os.getenv("PGPORT"), dbname=os.getenv("PGDATABASE"))
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM journal_entries WHERE user_id=%s;", (user_id,))
    entries = cursor.fetchall()
    connection.close()

    return render_template("entries.html", entries=entries)

@app.route('/forms/entries/add')
def add_entry_form():
    if session.get("user_id", ""):
        return render_template("add_entry.html")
    else:
       return redirect("/login")


@app.route('/api/entries/add', methods=['POST'])
def add_entry():
    title = request.form['title']
    content = request.form['content']
    user_id = session['user_id']

    # Analyze the sentiment
    sentiment = gpt_classify_sentiment(content)

    # Save the entry with the sentiment
    common.sql_write("INSERT INTO journal_entries (user_id, title, content, sentiment) VALUES (%s, %s, %s, %s);", [user_id, title, content, sentiment])

    return redirect('/entries')

@app.route('/forms/entries/edit/<entry_id>')
def edit_entry_form(entry_id):
    connection = psycopg2.connect(host=os.getenv("PGHOST"), user=os.getenv("JUSER"), password=os.getenv("PGPASSWORD"), port=os.getenv("PGPORT"), dbname=os.getenv("PGDATABASE"))
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM journal_entries WHERE entry_id=%s", (entry_id,))
    entry = cursor.fetchone()
    connection.close()

    if session.get("user_id", ""):
        return render_template('edit_entry.html', entry=entry)
    else:
        return redirect("/login")
    

@app.route('/api/entries/edit/<entry_id>', methods=['POST'])
def edit_entry(entry_id):
    title = request.form['title']
    content = request.form['content']

    # Analyze the sentiment
    sentiment = gpt_classify_sentiment(content, emotions)

    # Update the entry with the new sentiment
    common.sql_write("UPDATE journal_entries SET title=%s, content=%s, updated_at=CURRENT_TIMESTAMP, sentiment=%s WHERE entry_id=%s",
        [title, content, sentiment, entry_id])

    return redirect('/entries')

@app.route('/api/entries/delete/<entry_id>', methods=['POST'])
def delete_entry(entry_id):
    user_id = session["user_id"]
    common.sql_write("DELETE FROM journal_entries WHERE entry_id=%s AND user_id=%s", (entry_id, user_id))

    return redirect('/entries')

@app.route('/login')
def login_form():
  return render_template("login.html")

@app.route('/login', methods=['POST'])
def login_action():
    email = request.form.get('email')
    plain_text_password = request.form.get('password')

    curr_user = user.get_user_if_valid(email, plain_text_password)
    if curr_user:
        session["user_id"] = curr_user["id"]
        session["user_name"] = curr_user["user_name"]
        return redirect('/entries')
    else:
        return render_template("login_error.html")

@app.route("/logout")
def logout():
  session["user_id"] = None
  session["user_name"] = None
  return redirect("/login")

@app.route("/signup")
def signup():
  return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def signup_action():
  user.add_user(request.form.get("email"), request.form.get("user_name"), request.form.get("password"))
  return redirect("/login")

@app.route('/api/entries/<entry_id>/sentiment', methods=['POST'])
def analyze_sentiment(entry_id):
    # Get the journal entry text
    connection = psycopg2.connect(host=os.getenv("PGHOST"), user=os.getenv("JUSER"), password=os.getenv("PGPASSWORD"), port=os.getenv("PGPORT"), dbname=os.getenv("PGDATABASE"))
    cursor = connection.cursor()
    cursor.execute("SELECT content FROM journal_entries WHERE entry_id=%s", (entry_id,))
    content = cursor.fetchone()[0]
    connection.close()

    # Analyze the sentiment
    sentiment = gpt_classify_sentiment(content)

    # Return the sentiment as a JSON response
    return jsonify({"sentiment": sentiment})

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))





#button new note, onlick, second screen. 
#simple form, input heading for form 
#/chat route 
# text box towards the end/botton of screen. 
#user types in text box, presses sends. sends to flask app, aand then forward that input to chagpt, chatgpt sends you response, 
#users tab;e, notes table, message table, key table.
#how do you identify that a given record a reply, or original message was sent, how will you figure out the sequence of messages. 