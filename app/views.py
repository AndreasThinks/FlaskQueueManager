from flask import render_template, session, redirect
from app import app, db
from forms import LoginForm, AddTask
from models import User, Task



@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = AddTask()
    task_types = ["Penalty Ticket", "Found Property", "Crime Reporting","Lost Property", "Break"]
    x = 0
    task_types_dict = {}
    for task in task_types:
        new_dict = {x : task}
        task_types_dict.update(new_dict)
        x += 1
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
        task_types = task_types_dict,
        tasks = tasks)

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    try:
        tasker = session['new_task']
        t_number = tasker[0]
        name = tasker[1]
        task = Task(number= t_number, creator=235026, time = 20)
    except KeyError:
        task = Task(creator=200000, time=20)
    db.session.add(task)
    db.session.commit()
    return redirect('/index')

@app.route('/add_task_type', methods=['GET', 'POST'])
def add_task_type():
    all_tasks = Task.query.all()
    number = len(all_tasks)
    task_db = Task(id = number, type=task_type, creator = 235026, time=20)
    db.session.add(task_db)
    db.session.commit()
    return redirect('/index')