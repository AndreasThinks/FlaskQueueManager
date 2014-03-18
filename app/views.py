from flask import render_template
from app import app
from forms import AddTask



@app.route('/')
@app.route('/index', methods = ['GET', 'POST'])
def index():
    form = AddTask()
    user = { 'nickname': 'Dan'}  # fake user
    tasks = {1: 'passport', 2: 'eat', 3: 'Amazing'}
    return render_template("index.html",
        title = 'Home',
        user = user,
        form = form,
        tasks = tasks)