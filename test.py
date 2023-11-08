import sqlite3

# Connect to the SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect('school.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create table - COURSES
cursor.execute('''
CREATE TABLE IF NOT EXISTS courses(
   course_id INTEGER PRIMARY KEY,
   course_name TEXT NOT NULL,
   semester TEXT NOT NULL)
''')

# Create table - STUDENTS
cursor.execute('''
CREATE TABLE IF NOT EXISTS students(
   student_id INTEGER PRIMARY KEY,
   student_name TEXT NOT NULL,
   course_id INTEGER NOT NULL,
   FOREIGN KEY (course_id) REFERENCES courses (course_id))
''')

# Commit the changes
conn.commit()

# Close the connection
conn.close()
