
import sqlite3

DATABASE_NAME = 'healthcare_chatbot.db'

def execute_query(query, params=()):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor

def add_user(name, email, phone):
    query = "INSERT INTO user (name, email, phone) VALUES (?, ?, ?)"
    cursor = execute_query(query, (name, email, phone))
    return cursor.lastrowid

def add_symptom(user_id, description, assessment):
    query = "INSERT INTO symptom (user_id, description, assessment) VALUES (?, ?, ?)"
    execute_query(query, (user_id, description, assessment))

def add_appointment(user_id, doctor_name, appointment_datetime, status):
    query = "INSERT INTO appointment (user_id, doctor_name, appointment_datetime, status) VALUES (?, ?, ?, ?)"
    execute_query(query, (user_id, doctor_name, appointment_datetime, status))

def add_medication(user_id, name, dosage, reminder_time):
    query = "INSERT INTO medication (user_id, name, dosage, reminder_time) VALUES (?, ?, ?, ?)"
    execute_query(query, (user_id, name, dosage, reminder_time))

def get_user(user_id):
    query = "SELECT * FROM user WHERE id = ?"
    cursor = execute_query(query, (user_id,))
    return cursor.fetchone()

def get_symptoms(user_id):
    query = "SELECT * FROM symptom WHERE user_id = ?"
    cursor = execute_query(query, (user_id,))
    return cursor.fetchall()

def get_appointments(user_id):
    query = "SELECT * FROM appointment WHERE user_id = ?"
    cursor = execute_query(query, (user_id,))
    return cursor.fetchall()

def get_medications(user_id):
    query = "SELECT * FROM medication WHERE user_id = ?"
    cursor = execute_query(query, (user_id,))
    return cursor.fetchall()

def check_user_exists(email):
    query = "SELECT id FROM user WHERE email = ?"
    cursor = execute_query(query, (email,))
    result = cursor.fetchone()
    return result[0] if result else None