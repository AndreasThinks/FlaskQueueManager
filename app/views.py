from flask import render_template, session, redirect
from app import app, db
from forms import LoginForm, AddTask
from models import User, Task



@app.route('/')


@app.route('/index', methods=['GET', 'POST'])
def index():
    form = AddTask()
    user = { 'nickname': 'Dan'}  # fake user
    #tasks = {1: 'passport', 2: 'eat', 3: 'Amazing'}
    tasks = {}
    all_tasks = Task.query.all()
    i = 0
    for ta in all_tasks:
        new_dict = {i : ta.creator}
        i += 1
        tasks.update(new_dict)

    if form.validate_on_submit():
        session['new_task'] = [i, form.name.data]
        #task = Task(number=i, creator=235026, time = 20)
        #db.session.add(task)
        #db.session.commit()
        #return redirect('/index')
        return redirect('/add_task')
    return render_template("index.html",
        title = 'Home',
        user = user,
        form = form,
        tasks = tasks)

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    try:
        tasker = session['new_task']
        t_number = tasker[0]
        name = tasker[1]
        task = Task(number= t_number, creator=235026, time = 20)
    except KeyError:
        task = Task(number= 15, creator=200000, time = 20)
    db.session.add(task)
    db.session.commit()
    return redirect('/index')