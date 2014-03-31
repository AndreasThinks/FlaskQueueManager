from flask import render_template, session, redirect, request, flash, url_for, send_file
from app import app, db
from forms import LoginForm, AddTask, AddType, ReportForm, ResetDb, PasswordChange
from models import User, Task, Types
import datetime
import flask_login
import csv
from flask_login import login_required, logout_user

header_list = ["Task ID","User ID","Type","Weekday","Start Day","Start Month","Start Year","End Day","End Month","End Year","Start Hour","Start Minute","Minutes Taken"]

login_manager = flask_login.LoginManager()
login_manager.init_app(app)



@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


@app.route("/admin_tools", methods=["GET", "POST"])
@login_required
def admin_tools():
    current_user = flask_login.current_user
    if current_user.is_anonymous():
        is_admin = False
    else:
        is_admin = current_user.role == 1
    if is_admin == False:
        return redirect('')
    form = ResetDb()
    users = User.query.all()
    user_list = []
    for user in users:
        user_stats = [user.id, user.password, user.role]
        user_list.append(user_stats)
    if form.validate_on_submit() and form.confirm.data == "CONFIRM":
        for task in Task.query.all():
            db.session.delete(task)
            db.session.commit()
        for task in User.query.all():
            db.session.delete(task)
            db.session.commit()
        for type in Types.query.all():
            db.session.delete(type)
            db.session.commit()
        return redirect('')
    return render_template("admin_tools.html", form=form, users=user_list,anonymous=current_user.is_anonymous(), current_user=current_user,
        is_admin = is_admin)

@app.route("/delete_user")
@login_required
def delete_user():
    current_user = flask_login.current_user
    if current_user.is_anonymous():
        is_admin = False
    else:
        is_admin = current_user.role == 1
    if is_admin == False:
        return redirect('')
    user_id = request.args.get("user")
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/admin_tools')

@app.route("/edit_user")
@login_required
def edit_user():
    current_user = flask_login.current_user
    if current_user.is_anonymous():
        is_admin = False
    else:
        is_admin = current_user.role == 1
    if is_admin == False:
        return redirect('')
    form = PasswordChange()
    current_user = flask_login.current_user
    if current_user.is_anonymous():
        is_admin = False
    else:
        is_admin = current_user.role == 1
    user = request.args.get("user")
    role = User.query.get(user).role
    if role == 0:
        role_label = "basic"
    if role == 1:
        role_label = "admin"
    return render_template("edit_user.html", form=form, user=user, anonymous=current_user.is_anonymous(), role=role, role_label=role_label, current_user=current_user,
        is_admin = is_admin)


@app.route("/change_role")
@login_required
def change_role():
    current_user = flask_login.current_user
    if current_user.is_anonymous():
        is_admin = False
    else:
        is_admin = current_user.role == 1
    if is_admin == False:
        return redirect('')
    if flask_login.current_user.role == 1:
        user_id = request.args.get("user")
        user = User.query.get(user_id)
        if user.role == 0:
            user_role = 1
        if user.role == 1:
            user_role = 0
        user.role = user_role
        db.session.commit()
    return redirect('/admin_tools')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/index')

@app.route('/download_report')
@login_required
def download_report():
    file_name = 'report.csv'
    return send_file(file_name, as_attachment=True)

@app.route("/report", methods=["GET", "POST"])
@login_required
def report():
    form = ReportForm()
    current_user = flask_login.current_user
    if current_user.is_anonymous():
        is_admin = False
    else:
        is_admin = current_user.role == 1
    if form.validate_on_submit():
        if form.user.data == "000000":
            all_tasks = Task.query.all()
        if form.user.data != "000000":
            all_tasks = Task.query.filter_by(user_id=form.user.data)
        tasks_returned = []
        for task in all_tasks:
            if datetime.datetime(form.year_to.data, form.month_to.data, form.day_to.data) >= datetime.datetime(task.start_year, task.start_month, task.start_day) >= datetime.datetime(form.year_from.data, form.month_from.data, form.day_from.data):
                tasks_returned.append(task)
        task_list = []
        for task in tasks_returned:
            task_attributes=[task.id, task.user_id, task.type_label,task.start_weekday, task.start_day, task.start_month, task.start_year, task.end_day, task.end_month, task.end_year, task.start_hour, task.start_minute, task.time_taken]
            task_list.append(task_attributes)
        with open('app/report.csv', 'wb') as test_file:
            file_writer = csv.writer(test_file)
            file_writer.writerow(header_list)
            for task in task_list:
                file_writer.writerow(task)

        return render_template("generated_report.html", task_list=task_list, anonymous=current_user.is_anonymous(), user=form.user.data,tasks_returned=tasks_returned, current_user=current_user,
        is_admin = is_admin)
    return render_template("report.html", form=form, anonymous=current_user.is_anonymous(), current_user=current_user,
        is_admin = is_admin)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = LoginForm()
    current_user = flask_login.current_user
    if current_user.is_anonymous():
        is_admin = False
    else:
        is_admin = current_user.role == 1
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User(id=username, password=password, role=0)
        db.session.add(user)
        db.session.commit()
        flash("New User Registered")
        return redirect(url_for('index'))
    return render_template("register.html", form=form, current_user=current_user,anonymous=current_user.is_anonymous(),
        is_admin = is_admin)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    current_user = flask_login.current_user
    if current_user.is_anonymous():
        is_admin = False
    else:
        is_admin = current_user.role == 1
    user = flask_login.current_user
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if User.query.get(username).password == password:
            flask_login.login_user(User.query.get(username))
            flash("Logged in successfully.")
            return redirect(url_for("index"))
    return render_template("login.html", form=form, user=user, anonymous=current_user.is_anonymous(), current_user=current_user,
        is_admin = is_admin)

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    all_users = User.query.all()
    all_types = Types.query.all()
    if all_types == [] or None:
        pause = Types(type="Break", number=0)
        db.session.add(pause)
        db.session.commit()
    if all_users == [] or None:
        admin = User(id=222222, password='admin', role=1)
        db.session.add(admin)
        db.session.commit()
    form = AddTask()
    current_user = flask_login.current_user
    if current_user.is_anonymous():
        is_admin = False
    else:
        is_admin = current_user.role == 1
        all_tasks_user = Task.query.filter_by(user_id=current_user.id).all()
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
    tasks = {}
    all_tasks = Task.query.all()
    start_hour = 0
    start_minute = 0
    if not flask_login.current_user.is_anonymous():
        if len(all_tasks_user) > 1:
            #task_no = len(all_tasks) - 1
            all_tasks_user = Task.query.filter_by(user_id=current_user.id).all()
            task_no = len(all_tasks_user)
            task_no_type = all_tasks_user[-1].type_label
            previous_no = int(len(all_tasks) - 2)
            previous_task = Task.query.get(previous_no)
            start_hour = str(previous_task.end_hour)
            if len(start_hour) == 1:
                start_hour = "0" + start_hour
            start_minute = str(previous_task.end_minute)
            if len(start_minute) == 1:
                start_minute = "0" + start_minute
        else:
            task_no = None
            task_no_type = None
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
        task_no = task_no,
        task_no_type = task_no_type,
        form = form,
        task_types = task_types_dict,
        current_user=current_user,
        is_admin = is_admin,
        anonymous=current_user.is_anonymous(),
        tasks = tasks,
        start_hour=start_hour,
        start_minute=start_minute)

@app.route('/add_task', methods=['GET', 'POST'])
@login_required
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
    current_user = flask_login.current_user.id
    current_time = datetime.datetime.now()
    all_tasks = Task.query.all()
    task_type = int(request.args.get("task_type"))
    number = len(all_tasks)
    type_object = Types.query.filter_by(number=task_type).first()
    type_label = type_object.type
    task_to_db = Task(id=number, type=task_type, type_label=type_label, user_id=current_user, start_weekday=current_time.weekday(), start_day=current_time.day, start_month=current_time.month, start_year=current_time.year, start_minute=current_time.minute
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
        previous_delta = datetime.datetime(previous_task.end_year, previous_task.end_month, previous_task.end_day, previous_task.end_hour, previous_task.end_minute) - datetime.datetime(previous_task.start_year, previous_task.start_month, previous_task.start_day, previous_task.start_hour, previous_task.start_minute)
        previous_task.time_taken = previous_delta.seconds // 60
        #if previous_task.end_day != current_time.day:
         #   if 0 == current_time.hour - 1:
          #      previous_task.time_taken = (60 - previous_task.start_minute) + current_time.minute
           # else:
            #    previous_task.time_taken = (60 - previous_task.start_minute) + current_time.minute + (60 * ((current_time.hour - previous_task.start_hour) - 1))
        #if previous_task.end_day == current_time.day:
         #   if previous_task.start_hour == current_time.hour:
          #      previous_task.time_taken = current_time.minute - previous_task.start_minute
           # elif previous_task.start_hour == current_time.hour - 1:
            #    previous_task.time_taken = (60 - previous_task.start_minute) + current_time.minute
          #  else:
           #     previous_task.time_taken = (60 - previous_task.start_minute) + current_time.minute + (60 * ((current_time.hour - previous_task.start_hour) - 1))
        db.session.add(previous_task)

        #previous_task.end_time = Task(end_day=current_time.day, end_month=current_time.month, end_year=current_time.year, end_minute=current_time.minute
    #, end_hour=current_time.hour)

    db.session.commit()
    return redirect('/index')

@app.route('/types_admin', methods=['GET', 'POST'])
@login_required
def types_admin():
    form = AddType()
    user = { 'nickname': 'Dan'}  # fake user
    all_types = Types.query.all()
    current_user = flask_login.current_user
    if current_user.is_anonymous():
        is_admin = False
    else:
        is_admin = current_user.role == 1
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
                           current_user=current_user,
        is_admin = is_admin, anonymous=current_user.is_anonymous(),
                           task_types = task_types,
                           user = user,
                           form=form)

@app.route('/remove_type', methods=['GET', 'POST'])
@login_required
def remove_type():
    type_to_rm = request.args.get("type")
    type_to_rm = Types.query.get(type_to_rm)
    db.session.delete(type_to_rm)
    db.session.commit()
    return redirect('/types_admin')