import sqlite3
import time
import sys
import logging

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

# Function to get a database connection.
# This function connects to database with the name `database.db`
number_of_connection = 0
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    global number_of_connection
    number_of_connection +=1
    return connection

def logmsg(msg):
    date = time.asctime
    return f"{date}, {msg}"

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/healthz')
def healthcheck():
    response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
    )
    ## log line
    app.logger.debug('Debug Message')
    return response
@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    response = app.response_class(
            response=json.dumps({"db_connection_count": number_of_connection, "post_count": len(posts)}),
            status=200,
            mimetype='application/json'
    )
    ## log line
    app.logger.debug('Metrics request successfull')
    return response

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.debug(logmsg("A non-existing article is accessed and a 404 page is returned"))
      return render_template('404.html'), 404
    else:
      app.logger.debug(logmsg(f"Post \"{post['title']}\" was retrieved."))
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.debug(logmsg("'About Us' page is retrieved."))
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()

            return redirect(url_for('index'))

    return render_template('create.html')

# start the application on port 3111
if __name__ == "__main__":
   logging.basicConfig(level=logging.DEBUG,handlers=[logging.StreamHandler(sys.stdout), logging.StreamHandler(sys.stderr)])
   app.run(host='0.0.0.0', port='3111')