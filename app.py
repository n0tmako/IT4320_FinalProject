from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
import secrets

app = Flask(__name__)

# --- CONFIGURATION ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'final_project_files', 'reservations.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex(16) 

db = SQLAlchemy(app)

class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    passengerName = db.Column(db.String(100), nullable=False)
    seatRow = db.Column(db.Integer, nullable=False)
    seatColumn = db.Column(db.Integer, nullable=False) 
    eTicketNumber = db.Column(db.String(50), nullable=False)
    created = db.Column(db.DateTime)

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

# --- PROJECT LOGIC ---
def get_cost_matrix():
    """Returns a 12x4 matrix of seat prices"""
    cost_matrix = [[100, 75, 50, 100] for row in range(12)]
    return cost_matrix

def calculate_total_sales():
    """Calculates revenue based on existing reservations"""
    matrix = get_cost_matrix()
    total = 0
    reservations = Reservation.query.all()
    for res in reservations:
        # Subtracting 1 for 0-based matrix indexing
        total += matrix[res.seatRow][res.seatColumn]
    return total

def get_seating_chart():
    """Returns a 12x4 matrix indicating reserved and available seats"""
    seating_chart = [[None for col in range(4)] for row in range(12)]
    reservations = Reservation.query.all()
    for res in reservations:
        seating_chart[res.seatRow][res.seatColumn] = res
    return seating_chart

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reserve', methods=['GET', 'POST'])
def reserve():
    seating_chart = get_seating_chart()
    return render_template('reserve.html', seating_chart=seating_chart)

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

#--reservation logic--
import uuid
def generate_reservation_code():
    return str(uuid4()).split('-')[0].upper()
from flask import Flask, request, render_template
from models import db, Reservation
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservations.db'
db.init_app(app)
@app.route(' /reserve', methods=['GET', 'POST'])
def reserve():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        row = int(request.form['row'])
        column = int(request.form['column'])

        cost_matrix = [[100, 75, 50, 100] for _ in range(12)]
        price = cost_matrix[row][column]
        code = generate_reservation_code()

        new_reservation = Reservation(
            first_name=first_name,
            last_name=last_name,
            row=row,
            column=column,
            price=price,
            reservation_code=code
        )
        db.session.add(new_reservation)
        db.session.commit()
        return render_template('confirm.html', code=code)
    return render_template('reserve.html')
