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


@app.route('/')
def index():
    return render_template('index.html')    

@app.route('/admin/login', methods=['GET', 'POST'])
def adminLogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['admin_logged_in'] = True
            return redirect(url_for('adminDashboard'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('admin_login.html') 

@app.route('/admin/dashboard')
def adminLogout():
    session.pop('admin', None)
    return redirect(url_for('index')) 

@app.route("/admin/dashboard")
def adminDashboard():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    chart = loadSeatingChart()
    reservations = Reservation.query.all()
    total = sum(r.price for r in reservations)
    return render_template("admin_dashboard.html", chart=chart,
                           reservations=reservations, total=total)
 
 
@app.route("/reserve")
def reserve():
    return render_template("reserve.html")
