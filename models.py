from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin



db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)    
    first_name = db.Column(db.String(80), unique=True, nullable=True)
    last_name = db.Column(db.String(80), unique=True, nullable=False)  
    dob  = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(200), nullable=True)
    password = db.Column(db.String(200), nullable=True)
    role = db.Column(db.String(200), default="User")  # User role

    marketing_opt_out=db.Column(db.String(200), nullable=True)

    is_verified = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(6))
    # blocked = db.Column(db.Boolean, default=False)  # Blocked status
    # scores = db.relationship('Scores', backref='user', lazy=True)  # Relationship with scores
    
    # def is_active(self):
    #      return not self.blocked  # Users are active unless blocked

    # def get_id(self):
    #      return str(self.id)  # Flask-Login requires a string ID
