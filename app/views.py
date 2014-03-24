from flask import render_template, session, redirect, request
from app import app, db
from forms import LoginForm, AddTask, AddType
from models import User, Task, Types
import datetime



@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = AddTask()
    all_types = Types.query.all()
    task_types = []
    for item in all_types:
        task_types.append(item.type)
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
    if len(all_tasks) > 0:
        task_no = len(all_tasks) - 1
        task_no_type = task_types_dict[all_tasks[len(all_tasks)-1].type]
    else:
        task_no = None
        task_no_type = None
    i = 0
    for ta in all_tasks:
        new_dict = {i : ta.creator}
        i += 1
        tasks.update(new_dict)


    #if form.validate_on_submit():
     #   session['new_task'] = [i, form.name.data]
        #task = Task(number=i, creator=235026, time = 20)
        #db.session.add(task)
        #db.session.commit()
        #return redirect('/index')
      #  return redirect('/add_task')
    return render_template("index.html",
        title = 'Home',
        user = user,
        task_no = task_no,
        task_no_type = task_no_type,
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
    current_time = datetime.datetime.now()
    all_tasks = Task.query.all()
    task_type = int(request.args.get("task_type"))
    number = len(all_tasks)
    task_to_db = Task(id=number, type=task_type, user_id=235026, start_day=current_time.day, start_month=current_time.month, start_year=current_time.year, start_minute=current_time.minute
    , start_hour=current_time.hour)
    db.session.add(task_to_db)

    if number > 0:
        previous_no = number - 1
        previous_task = Task.query.get(previous_no)
        previous_task.end_day = current_time.day
        previous_task.end_minute = current_time.minute
        previous_task.end_hour = current_time.hour
        previous_task.end_month = current_time.month
        previous_task.end_year = current_time.year
        if previous_task.end_day != current_time.day:
            if 0 == current_time.hour - 1:
                previous_task.time_taken = (60 - previous_task.start_minute) + current_time.minute
            else:
                previous_task.time_taken = (60 - previous_task.start_minute) + current_time.minute + (60 * ((current_time.hour - previous_task.start_hour) - 1))
        db.session.add(
        if previous_task.end_day == current_time.day:
            if previous_task.start_hour == current_time.hour:
                previous_task.time_taken = current_time.minute - previous_task.start_minute
            elif previous_task.start_hour == current_time.hour - 1:
                previous_task.time_taken = (60 - previous_task.start_minute) + current_time.minute
            else:
                previous_task.time_taken = (60 - previous_task.start_minute) + current_time.minute + (60 * ((current_time.hour - previous_task.start_hour) - 1))
        db.session.add(previous_task)

        #previous_task.end_time = Task(end_day=current_time.day, end_month=current_time.month, end_year=current_time.year, end_minute=current_time.minute
    #, end_hour=current_time.hour)

    db.session.commit()
    return redirect('/index')

@app.route('/types_admin', methods=['GET', 'POST'])
def types_admin():
    form = AddType()
    user = { 'nickname': 'Dan'}  # fake user
    all_types = Types.query.all()
    task_types = []
    for item in all_types:
        task_types.append(item.type)
    if form.validate_on_submit():
        type_data = form.type.data
        type_db = Types(type=type_data, number=len(all_types))
        db.session.add(type_db)
        db.session.commit()
        return redirect('/types_admin')

    return render_template("types_admin.html",
                           task_types = task_types,
                           user = user,
                           form=form)