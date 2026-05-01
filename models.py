from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    row = db.Column(db.Integer, nullable=False)
    column = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    reservation_code = db.Column(db.String(20), unique=True, nullable=False)


class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
