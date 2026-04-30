from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy(app)

class Reservation(db.model):
    _tablename__ = 'reservations'
    id = db.column(db.integer, primary_key=True)
    firstName = db.column(db.string(50), nullable=False)
    lastName = db.column(db.string(50), nullable=False)
    seatRow = db.column(db.integer, nullable=False)
    seatColumn = db.column(db.integer, nullable=False) 
    ResCode = db.column(db.string(10), nullable=False, unique=True) 
    price = db.column(db.float, nullable=False) 

def getCost():
    return [[100, 75, 50, 100] for _ in range(12)] 

def loadSeatingChart():
    chart  = [[None] * 4 for _ in range(12)]
    for r in Reservation.query.all():
        chart[r.seatRow - 1][r.seatColumn -1] = r
    return chart

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"
