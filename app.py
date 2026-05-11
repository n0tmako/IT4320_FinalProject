from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
import secrets
import uuid

app = Flask(__name__)

# --- CONFIGURATION ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'final_project_files', 'reservations.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex(16) 

db = SQLAlchemy(app)

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
        total += matrix[res.row - 1][res.column - 1]
    return total

def get_seating_chart():
    """Returns a 12x4 matrix indicating reserved and available seats"""
    seating_chart = [[None for col in range(4)] for row in range(12)]
    reservations = Reservation.query.all()
    for res in reservations:
        seating_chart[res.row - 1][res.column - 1] = res
    return seating_chart

def generate_reservation_code():
    """Generate a unique reservation code"""
    return str(uuid.uuid4()).split('-')[0].upper()

# --- ROUTES ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reserve', methods=['GET', 'POST'])
def reserve():
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        row = int(request.form.get('row'))
        column = int(request.form.get('column'))
        
        # Check if seat is already reserved
        existing_reservation = Reservation.query.filter_by(row=row, column=column).first()
        if existing_reservation:
            flash('This seat is already reserved', 'error')
            return redirect(url_for('reserve'))
        
        cost_matrix = get_cost_matrix()
        price = cost_matrix[row - 1][column - 1]
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
        
        session['reservation_code'] = code
        session['price'] = price
        return redirect(url_for('checkout'))
    
    seating_chart = get_seating_chart()
    return render_template('reserve.html', seating_chart=seating_chart)

@app.route('/checkout')
def checkout():
    code = session.get('reservation_code')
    price = session.get('price')
    if not code:
        return redirect(url_for('reserve'))
    return render_template('checkout.html', code=code, price=price)

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username, password=password).first()
        if admin:
            session['admin_logged_in'] = True
            session['admin_id'] = admin.id
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('admin.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    reservations = Reservation.query.all()
    total_reservations = len(reservations)
    occupied_seats = total_reservations
    total_sales = calculate_total_sales()
    avg_price = (total_sales / total_reservations) if total_reservations > 0 else 0
    seating_chart = get_seating_chart()
    
    return render_template('dashboard.html', 
                         reservations=reservations, 
                         total_reservations=total_reservations,
                         occupied_seats=occupied_seats,
                         total_sales=total_sales,
                         avg_price=avg_price,
                         seating_chart=seating_chart)

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/admin/delete/<int:res_id>', methods=['POST'])
def admin_delete(res_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    reservation = Reservation.query.get_or_404(res_id)
    db.session.delete(reservation)
    db.session.commit()
    flash('Reservation deleted successfully', 'info')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
