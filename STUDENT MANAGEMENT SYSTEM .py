import sqlite3
from datetime import datetime

DB_NAME = "student_management.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Create Students table
    c.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT
        )
    ''')

    # Create Attendance table
    c.execute('''
        CREATE TABLE IF NOT EXISTS Attendance (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('Present', 'Absent', 'Late')),
            FOREIGN KEY(student_id) REFERENCES Students(student_id)
        )
    ''')

    # Create Grades table
    c.execute('''
        CREATE TABLE IF NOT EXISTS Grades (
            grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            grade TEXT NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY(student_id) REFERENCES Students(student_id)
        )
    ''')

    # Create Messages table
    c.execute('''
        CREATE TABLE IF NOT EXISTS Messages (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            receiver TEXT NOT NULL,
            message TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def add_student(first_name, last_name, email, phone=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO Students (first_name, last_name, email, phone)
            VALUES (?, ?, ?, ?)
        ''', (first_name, last_name, email, phone))
        conn.commit()
        print("Student added successfully.")
    except sqlite3.IntegrityError:
        print("Error: A student with this email already exists.")
    finally:
        conn.close()

def list_students():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT student_id, first_name, last_name, email, phone FROM Students')
    students = c.fetchall()
    conn.close()
    if students:
        print("Students:")
        for s in students:
            print(f"ID: {s[0]}, Name: {s[1]} {s[2]}, Email: {s[3]}, Phone: {s[4]}")
    else:
        print("No students found.")

def record_attendance(student_id, date, status):
    if status not in ('Present', 'Absent', 'Late'):
        print("Invalid status. Use 'Present', 'Absent', or 'Late'.")
        return
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT student_id FROM Students WHERE student_id = ?', (student_id,))
    if not c.fetchone():
        print("Student ID not found.")
        conn.close()
        return
    c.execute('''
        INSERT INTO Attendance (student_id, date, status)
        VALUES (?, ?, ?)
    ''', (student_id, date, status))
    conn.commit()
    conn.close()
    print("Attendance recorded.")

def view_attendance(student_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT date, status FROM Attendance
        WHERE student_id = ?
        ORDER BY date DESC
    ''', (student_id,))
    records = c.fetchall()
    conn.close()
    if records:
        print(f"Attendance records for student ID {student_id}:")
        for r in records:
            print(f"Date: {r[0]}, Status: {r[1]}")
    else:
        print("No attendance records found for this student.")

def add_grade(student_id, subject, grade, date):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT student_id FROM Students WHERE student_id = ?', (student_id,))
    if not c.fetchone():
        print("Student ID not found.")
        conn.close()
        return
    c.execute('''
        INSERT INTO Grades (student_id, subject, grade, date)
        VALUES (?, ?, ?, ?)
    ''', (student_id, subject, grade, date))
    conn.commit()
    conn.close()
    print("Grade added.")

def view_grades(student_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT subject, grade, date FROM Grades
        WHERE student_id = ?
        ORDER BY date DESC
    ''', (student_id,))
    records = c.fetchall()
    conn.close()
    if records:
        print(f"Grades for student ID {student_id}:")
        for r in records:
            print(f"Subject: {r[0]}, Grade: {r[1]}, Date: {r[2]}")
    else:
        print("No grades found for this student.")

def send_message(sender, receiver, message):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO Messages (sender, receiver, message, date)
        VALUES (?, ?, ?, ?)
    ''', (sender, receiver, message, date))
    conn.commit()
    conn.close()
    print("Message sent.")

def view_messages(user1, user2):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT sender, receiver, message, date FROM Messages
        WHERE (sender = ? AND receiver = ?) OR (sender = ? AND receiver = ?)
        ORDER BY date DESC
    ''', (user1, user2, user2, user1))
    messages = c.fetchall()
    conn.close()
    if messages:
        print(f"Messages between {user1} and {user2}:")
        for m in messages:
            print(f"[{m[3]}] {m[0]} -> {m[1]}: {m[2]}")
    else:
        print("No messages found between these users.")

def main_menu():
    create_tables()
    while True:
        print("\nStudent Management System")
        print("1. Add Student")
        print("2. List Students")
        print("3. Record Attendance")
        print("4. View Attendance")
        print("5. Add Grade")
        print("6. View Grades")
        print("7. Send Message")
        print("8. View Messages")
        print("9. Exit")

        choice = input("Enter your choice (1-9): ")

        if choice == '1':
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            email = input("Email: ")
            phone = input("Phone (optional): ")
            add_student(first_name, last_name, email, phone if phone else None)
        elif choice == '2':
            list_students()
        elif choice == '3':
            student_id = input("Student ID: ")
            date = input("Date (YYYY-MM-DD) [leave blank for today]: ")
            if not date:
                date = datetime.now().strftime("%Y-%m-%d")
            status = input("Status (Present/Absent/Late): ")
            record_attendance(int(student_id), date, status)
        elif choice == '4':
            student_id = input("Student ID: ")
            view_attendance(int(student_id))
        elif choice == '5':
            student_id = input("Student ID: ")
            subject = input("Subject: ")
            grade = input("Grade: ")
            date = input("Date (YYYY-MM-DD) [leave blank for today]: ")
            if not date:
                date = datetime.now().strftime("%Y-%m-%d")
            add_grade(int(student_id), subject, grade, date)
        elif choice == '6':
            student_id = input("Student ID: ")
            view_grades(int(student_id))
        elif choice == '7':
            sender = input("Sender (e.g., teacher, parent): ")
            receiver = input("Receiver (e.g., student, parent): ")
            message = input("Message: ")
            send_message(sender, receiver, message)
        elif choice == '8':
            user1 = input("User 1: ")
            user2 = input("User 2: ")
            view_messages(user1, user2)
        elif choice == '9':
            print("Exiting Student Management System.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 9.")

if __name__ == "__main__":
    main_menu()
