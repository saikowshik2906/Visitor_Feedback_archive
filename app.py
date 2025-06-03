import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)

# Configuration
app.secret_key = 'visitor_feedback_secret_key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'  # Replace with your actual MySQL password
app.config['MYSQL_DB'] = 'visitor_feedback'
app.config['MYSQL_AUTOCOMMIT'] = True  # Enable autocommit

# Initialize MySQL
mysql = MySQL(app)

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
        submission_date = datetime.now()
        
        # Insert into database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'INSERT INTO feedback (name, email, feedback_text, rating, submission_date) VALUES (%s, %s, %s, %s, %s)',
            (name, email, feedback_text, rating, submission_date)
        )
        mysql.connection.commit()
        cursor.close()
        
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
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE username = %s', (username,))
        account = cursor.fetchone()
        cursor.close()
        
        if account and check_password_hash(account['password'], password):
            session['loggedin'] = True
            session['username'] = account['username']
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Incorrect username/password!', 'danger')
            return redirect(url_for('admin_login'))
    
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'loggedin' not in session:
        return redirect(url_for('admin_login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM feedback ORDER BY submission_date DESC')
    feedback_list = cursor.fetchall()
    cursor.close()
    
    return render_template('admin_dashboard.html', feedback_list=feedback_list)

@app.route('/admin/mark_as_read/<int:id>')
def mark_as_read(id):
    if 'loggedin' not in session:
        return redirect(url_for('admin_login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE feedback SET status = "read" WHERE id = %s', (id,))
    mysql.connection.commit()
    cursor.close()
    
    flash('Feedback marked as read!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/archive_feedback/<int:id>')
def archive_feedback(id):
    if 'loggedin' not in session:
        return redirect(url_for('admin_login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE feedback SET status = "archived" WHERE id = %s', (id,))
    mysql.connection.commit()
    cursor.close()
    
    flash('Feedback archived successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_feedback/<int:id>')
def delete_feedback(id):
    if 'loggedin' not in session:
        return redirect(url_for('admin_login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM feedback WHERE id = %s', (id,))
    mysql.connection.commit()
    cursor.close()
    
    flash('Feedback deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
