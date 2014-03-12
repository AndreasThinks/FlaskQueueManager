from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'Dan'}  # fake user
    tasks = {1: 'passport', 2: 'eat', 3: 'Amazing'}
    return render_template("index.html",
        title = 'Home',
        user = user,
        tasks = tasks)