import MySQLdb
import os
from werkzeug.security import generate_password_hash
import sys

def init_db():
    try:
        # Connect to MySQL server
        connection = MySQLdb.connect(
            host='localhost',
            user='root',
            password='your_mysql_password'  # Replace with your actual MySQL password
        )
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS visitor_feedback")
        cursor.execute("USE visitor_feedback")
        
        # Create feedback table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            feedback_text TEXT NOT NULL,
            rating INT NOT NULL,
            submission_date DATETIME NOT NULL,
            status ENUM('new', 'read', 'archived') DEFAULT 'new'
        )
        """)
        
        # Create admin table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Check if admin user exists
        cursor.execute("SELECT * FROM admin WHERE username = 'admin'")
        admin = cursor.fetchone()
        
        # If admin doesn't exist, create it
        if not admin:
            password_hash = generate_password_hash('admin123')
            cursor.execute(
                "INSERT INTO admin (username, password) VALUES (%s, %s)",
                ('admin', password_hash)
            )
            print("Default admin user created: username=admin, password=admin123")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("Database initialized successfully!")
        
        # Import and run test data script
        try:
            import test_data
            test_data.insert_test_data()
        except ImportError:
            # If we're running from a different directory, adjust the path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            sys.path.append(current_dir)
            import test_data
            test_data.insert_test_data()
        
        return True
    
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False

if __name__ == "__main__":
    init_db()
