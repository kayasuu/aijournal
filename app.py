from flask import Flask, render_template, request, redirect, session, jsonify
from models import common, user
from sentiment_analysis import gpt_classify_sentiment
import os
import openai
import bcrypt
import psycopg2


app = Flask(__name__)

openai.api_key = os.getenv("KEY")

# app.config['SECRET_KEY'] = "SECRET"
my_secret_key=os.getenv("SECRET_KEY")
app.config['SECRET_KEY'] = my_secret_key


@app.route('/')
def index():
    if not session.get("user_id", ""):
        return redirect("/login")
    else:
       return redirect("/entries")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/entries')
def entries():
    #Checks if there is a user_id stored in the user's session data. No user_id means the user is not logged in.
    if not session.get("user_id", ""):
        return redirect("/login")

    #If the user is logged in, this line gets the user_id from the session data.
    user_id = session["user_id"]

    #Fetches all entries from the 'journal_entries' table in the database that belong to the logged-in user, sorted by the 'updated_at' field in descending order
    entries = common.sql_read("SELECT * FROM journal_entries WHERE user_id=%s ORDER BY updated_at DESC;", (user_id,))
    
    #Renders entries.html' template, passing the fetched journal entries to the template
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

    #Get AI advice based on user's journal entry, and add it to user's entries database. 
    sentiment = gpt_classify_sentiment(content)
    common.sql_write("INSERT INTO journal_entries (user_id, title, content, sentiment) VALUES (%s, %s, %s, %s);", [user_id, title, content, sentiment])

    return redirect('/entries')

@app.route('/forms/entries/edit/<entry_id>')
def edit_entry_form(entry_id):

    #Select user's journal entry by ID, and then if user is logged in display the page with their previous entry and AI feedback

    connection = psycopg2.connect(host=os.getenv("PGHOST"), user=os.getenv("JUSER"), password=os.getenv("PGPASSWORD"), port=os.getenv("PGPORT"), dbname=os.getenv("PGDATABASE"))
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM journal_entries WHERE entry_id=%s", (entry_id,))
    entry = cursor.fetchone()
    connection.close()

    if session.get("user_id", ""):
        entries = common.sql_read("SELECT * FROM journal_entries WHERE user_id=%s AND entry_id=%s;", (session.get("user_id"), entry_id,))
        return render_template('edit_entry.html', entry=entry, entries=entries)
    else:
        return redirect("/login")
    

@app.route('/api/entries/edit/<entry_id>', methods=['POST'])
def edit_entry(entry_id):

    #Update the journal entry with new title, content and AI generated feedback. 

    title = request.form['title']
    content = request.form['content']

    sentiment = gpt_classify_sentiment(content)

    common.sql_write("UPDATE journal_entries SET title=%s, content=%s, updated_at=CURRENT_TIMESTAMP, sentiment=%s WHERE entry_id=%s",
        [title, content, sentiment, entry_id])

    return redirect('/entries')

@app.route('/api/entries/delete/<entry_id>', methods=['POST'])
def delete_entry(entry_id):

    #Delete entry

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

    #if login details are valid, declare session as under userID+username. 

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

    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))