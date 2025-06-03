CREATE DATABASE IF NOT EXISTS visitor_feedback;
USE visitor_feedback;

-- Table for storing visitor feedback
CREATE TABLE IF NOT EXISTS feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    feedback_text TEXT NOT NULL,
    rating INT NOT NULL,
    submission_date DATETIME NOT NULL,
    status ENUM('new', 'read', 'archived') DEFAULT 'new'
);

-- Table for admin users
CREATE TABLE IF NOT EXISTS admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Insert a default admin user (username: admin, password: admin123)
-- In a real application, you would use a more secure password
INSERT INTO admin (username, password) VALUES 
('admin', '$2b$12$8kOuFeJBjnGKkozlKXexv.pOiHQ1AKz0CKNVVUMbm3YnYmGFGVlMm');
