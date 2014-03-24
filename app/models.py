from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(10))
    tasks = db.relationship('Task', backref = 'creator', lazy = 'dynamic')

    def __repr__(self):
        return '<User %r>' % (self.id)

    def get_id(self):
        return unicode(self.id)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.Integer)
    user_id = db.Column(db.String(120), db.ForeignKey('user.id'))
    start_day = db.Column(db.Integer)
    start_month = db.Column(db.Integer)
    start_year = db.Column(db.Integer)
    start_hour = db.Column(db.Integer)
    start_minute = db.Column(db.Integer)
    end_day = db.Column(db.Integer)
    end_month = db.Column(db.Integer)
    end_year = db.Column(db.Integer)
    end_hour = db.Column(db.Integer)
    end_minute = db.Column(db.Integer)
    time_taken = db.Column(db.SmallInteger)


    def __repr__(self):
        return '<Task %r>' % (self.id)

class Types(db.Model):
    type = db.Column(db.String, primary_key = True)
    number = db.Column(db.Integer)

    def __repr__(self):
        return '<Type %r>' % (self.type)