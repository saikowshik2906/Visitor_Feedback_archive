import MySQLdb
from datetime import datetime, timedelta
import random

# Sample feedback data
sample_feedback = [
    {
        "name": "John Smith",
        "email": "john.smith@example.com",
        "feedback_text": "The service was excellent. I enjoyed my visit and will definitely come back again. The staff was very friendly and helpful.",
        "rating": 5,
        "status": "new"
    },
    {
        "name": "Emily Johnson",
        "email": "emily.johnson@example.com",
        "feedback_text": "Good experience overall, but the waiting time was a bit long. Everything else was great though.",
        "rating": 4,
        "status": "new"
    },
    {
        "name": "Michael Brown",
        "email": "michael.brown@example.com",
        "feedback_text": "Average experience. Some things could be improved, like the cleanliness of the facility.",
        "rating": 3,
        "status": "read"
    },
    {
        "name": "Sarah Davis",
        "email": "sarah.davis@example.com",
        "feedback_text": "Not satisfied with my visit. The staff was not very helpful and I had to wait for a long time.",
        "rating": 2,
        "status": "read"
    },
    {
        "name": "Robert Wilson",
        "email": "robert.wilson@example.com",
        "feedback_text": "Terrible experience. I will not be returning and would not recommend to others.",
        "rating": 1,
        "status": "archived"
    },
    {
        "name": "Jennifer Taylor",
        "email": "jennifer.taylor@example.com",
        "feedback_text": "Excellent facility and great staff. Everything was perfect from start to finish.",
        "rating": 5,
        "status": "new"
    },
    {
        "name": "David Anderson",
        "email": "david.anderson@example.com",
        "feedback_text": "Very good experience. Staff was professional and the facilities were clean.",
        "rating": 4,
        "status": "read"
    }
]

def insert_test_data():
    try:        # Connect to MySQL server
        connection = MySQLdb.connect(
            host='localhost',
            user='root',
            password='your_mysql_password',  # Replace with your actual MySQL password
            db='visitor_feedback'
        )
        cursor = connection.cursor()
        
        # Check if we already have data
        cursor.execute("SELECT COUNT(*) FROM feedback")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print("Test data already exists. Skipping insertion.")
            return
        
        # Insert sample feedback with different dates
        now = datetime.now()
        
        for i, feedback in enumerate(sample_feedback):
            # Create a date between 1-30 days ago
            days_ago = random.randint(1, 30)
            submission_date = now - timedelta(days=days_ago)
            
            cursor.execute(
                'INSERT INTO feedback (name, email, feedback_text, rating, submission_date, status) VALUES (%s, %s, %s, %s, %s, %s)',
                (
                    feedback["name"],
                    feedback["email"],
                    feedback["feedback_text"],
                    feedback["rating"],
                    submission_date,
                    feedback["status"]
                )
            )
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print(f"Successfully inserted {len(sample_feedback)} sample feedback records.")
        return True
    
    except Exception as e:
        print(f"Error inserting test data: {e}")
        return False

if __name__ == "__main__":
    insert_test_data()
