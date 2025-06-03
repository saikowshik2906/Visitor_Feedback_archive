import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)

# Configuration
app.secret_key = 'visitor_feedback_secret_key'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'visitor_feedback.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Models
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    submission_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.String(20), nullable=False, default='new')

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

# Create database tables
with app.app_context():
    db.create_all()
    # Check if admin user exists
    admin = Admin.query.filter_by(username='admin').first()
    if not admin:
        # Create default admin user
        admin = Admin(
            username='admin',
            password=generate_password_hash('admin123')
        )
        db.session.add(admin)
        db.session.commit()
        print("Default admin user created: username=admin, password=admin123")

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_feedback', methods=['GET', 'POST'])
def submit_feedback():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        feedback_text = request.form['feedback']
        rating = request.form['rating']
        
        # Create new feedback
        new_feedback = Feedback(
            name=name,
            email=email,
            feedback_text=feedback_text,
            rating=rating,
            submission_date=datetime.now()
        )
        
        # Add to database
        db.session.add(new_feedback)
        db.session.commit()
        
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('index'))
    
    return render_template('submit_feedback.html')

@app.route('/admin')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if user exists
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and check_password_hash(admin.password, password):
            session['loggedin'] = True
            session['username'] = admin.username
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Incorrect username/password!', 'danger')
            return redirect(url_for('admin_login'))
    
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'loggedin' not in session:
        return redirect(url_for('admin_login'))
    
    # Get all feedback
    feedback_list = Feedback.query.order_by(Feedback.submission_date.desc()).all()
    
    return render_template('admin_dashboard.html', feedback_list=feedback_list)

@app.route('/admin/mark_as_read/<int:id>')
def mark_as_read(id):
    if 'loggedin' not in session:
        return redirect(url_for('admin_login'))
    
    feedback = Feedback.query.get_or_404(id)
    feedback.status = 'read'
    db.session.commit()
    
    flash('Feedback marked as read!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/archive_feedback/<int:id>')
def archive_feedback(id):
    if 'loggedin' not in session:
        return redirect(url_for('admin_login'))
    
    feedback = Feedback.query.get_or_404(id)
    feedback.status = 'archived'
    db.session.commit()
    
    flash('Feedback archived successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_feedback/<int:id>')
def delete_feedback(id):
    if 'loggedin' not in session:
        return redirect(url_for('admin_login'))
    
    feedback = Feedback.query.get_or_404(id)
    db.session.delete(feedback)
    db.session.commit()
    
    flash('Feedback deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
