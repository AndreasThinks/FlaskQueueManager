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
    time = db.Column(db.SmallInteger)

    def __repr__(self):
        return '<Task %r>' % (self.number)