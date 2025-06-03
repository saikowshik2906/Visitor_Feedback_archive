# Visitor Feedback Archive System

A web application built with Flask, MySQL, and HTML/CSS for collecting, managing, and archiving visitor feedback.

## Features

- **Feedback Submission**: Visitors can submit feedback with ratings.
- **Admin Dashboard**: Secure interface for viewing and managing feedback.
- **Feedback Management**: Mark as read, archive, or delete feedback entries.
- **Responsive Design**: Works on desktop and mobile devices.

## Prerequisites

- Python 3.7+
- MySQL Server
- pip (Python package manager)

## Installation

1. Clone the repository:

   ```
   git clone [[repository-url]](https://github.com/saikowshik2906/Visitor_Feedback_archive.git)
   cd visitor_feedback_archive
   ```

2. Install required packages:

   ```
   pip install -r requirements.txt
   ```

3. Set up the database:

   ```
   python database/init_db.py
   ```

4. Run the application:

   ```
   python app_sqlite.py
   ```

5. Access the application:
   - Open your browser and navigate to `http://localhost:5000`
   - Admin login: username: `admin`, password: `admin123`

## Project Structure

- `app.py`: Main Flask application
- `database/`: Contains database setup and initialization scripts
- `static/`: CSS and other static files
- `templates/`: HTML templates for the application

## Screenshots

(Add screenshots here)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
