import sqlite3


def create_database():
    conn = sqlite3.connect("prediction_history.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            age INTEGER,
            gender TEXT,
            department TEXT,
            job_role TEXT,
            prediction TEXT,
            stay_probability REAL,
            leave_probability REAL
        )
    """)

    conn.commit()
    conn.close()

def save_prediction(
    date,
    age,
    gender,
    department,
    job_role,
    prediction,
    stay_probability,
    leave_probability
):

    conn = sqlite3.connect("prediction_history.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions(
            date,
            age,
            gender,
            department,
            job_role,
            prediction,
            stay_probability,
            leave_probability
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        date,
        age,
        gender,
        department,
        job_role,
        prediction,
        stay_probability,
        leave_probability
    ))
    

    conn.commit()
    conn.close()
def get_prediction_history():

    conn = sqlite3.connect("prediction_history.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM predictions
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows
def clear_prediction_history():

    conn = sqlite3.connect("prediction_history.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM predictions")

    conn.commit()
    conn.close()