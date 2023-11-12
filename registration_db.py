import sqlite3

# Connect to the SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect('registration.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create table - STUDENTS
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
   student_id INTEGER PRIMARY KEY,
   firstname TEXT NOT NULL,
   lastname TEXT NOT NULL, 
   major TEXT NOT NULL, 
   gpa REAL
)
''')

# Add Values - STUDENTS
cursor.execute('''
INSERT INTO students (student_id, firstname, lastname, major, gpa) 
VALUES
   (123456, 'John', 'Doe', 'Computer Science', 3.65),
   (987654, 'Jane', 'Doe', 'Biology', 3.22),
   (456789, 'Alice', 'Smith', 'History', 2.06),
   (543210, 'Bob', 'Johnson', 'Mathematics', 1.56),
   (654321, 'Eva', 'Williams', 'Physics', 2.89),
   (345678, 'Charlie', 'Brown', 'Psychology', 3.89),
   (876543, 'Grace', 'White', 'Chemistry', 2.22),
   (234567, 'David', 'Davis', 'English', 3.12),
   (789012, 'Olivia', 'Miller', 'Economics', 3.42),
   (678901, 'Liam', 'Taylor', 'Sociology', 1.20);         
'''
)

# Create table - COURSES
cursor.execute('''
CREATE TABLE IF NOT EXISTS courses (
   course_name TEXT NOT NULL PRIMARY KEY,
   location TEXT NOT NULL,
   description TEXT NOT NULL,
   hours INTEGER
)
''')

# Add Values - COURSES
cursor.execute('''
INSERT INTO courses (course_name, location, description, hours)
VALUES
   ('CIS 475', 'Bradley Hall', 'Computer Infrastructure', 3),
   ('CIS 430', 'Bradley Hall', 'Networking', 3),
   ('BIO 292', 'Olin', 'Human Anatomy', 6),
   ('CHEM 101', 'Olin', 'Intro to Chem', 3),
   ('CS 140', 'Bradley Hall', 'Java Programming', 3),
   ('ENT 280', 'BECC', 'Entreprenuership', 1),
   ('COM 103', 'GCC', 'Oral Communication', 3),
   ('COM 292', 'GCC', 'Organizational Communication', 3),
   ('CS 475', 'Bradley Hall', 'Computer Information Systems', 6),
   ('MIS 173', 'BECC', 'Intro to Business Analytics', 1),
   ('MTH 111', 'Bradley Hall', 'Precalculus', 3);          
'''
)

# Create table - SEMESTER
cursor.execute('''
CREATE TABLE IF NOT EXISTS semesters (
   semester TEXT NOT NULL PRIMARY KEY,
   start_date DATE,
   end_date DATE,
   year INTEGER 
)
''')

# Add values - SEMESTER
cursor.execute('''
INSERT INTO semesters (semester, start_date, end_date, year)
VALUES
   ('Spring 2023', '2023-01-15', '2023-05-15', 2023),
   ('Summer 2023', '2023-06-01', '2023-08-31', 2023),
   ('Fall 2023', '2023-09-01', '2023-12-15', 2023),
   ('Spring 2024', '2024-01-15', '2024-05-15', 2024),
   ('Summer 2024', '2024-06-01', '2024-08-31', 2024),
   ('Fall 2024', '2024-09-01', '2024-12-15', 2024),
   ('Spring 2025', '2025-01-15', '2025-05-15', 2025),
   ('Summer 2025', '2025-06-01', '2025-08-31', 2025),
   ('Fall 2025', '2025-09-01', '2025-12-15', 2025),
   ('Spring 2026', '2026-01-15', '2026-05-15', 2026);
''')

# Create table - INSTRUCTORS
cursor.execute('''
CREATE TABLE IF NOT EXISTS instructors (
   instructor_name TEXT NOT NULL PRIMARY KEY,
   office_number INTEGER,
   department TEXT NOT NULL,
   email TEXT NOT NULL
)
''')

# Add values - INSTRUCTORS
cursor.execute('''
INSERT INTO instructors (instructor_name, office_number, department, email)
VALUES
   ('Smith Johnson', 101, 'Foster College of Business', 'smith.johnson@example.com'),
   ('Emma Johnson', 050, 'Foster College of Business', 'emma.johnson@example.com'),
   ('Emily Davis', 202, 'Slane College of Communications and Fine Arts', 'emily.davis@example.com'),
   ('Alex Martin', 303, 'College of Education and Health Sciences', 'alex.martin@example.com'),
   ('Olivia Thompson', 404, 'Caterpillar College of Engineering and Technology', 'olivia.thompson@example.com'),
   ('Daniel Harris', 505, 'College of Liberal Arts and Sciences', 'daniel.harris@example.com'),
   ('Sophia Nelson', 606, 'Graduate Education', 'sophia.nelson@example.com'),
   ('Liam Lewis', 707, 'Academic Exploration Program', 'liam.lewis@example.com'),
   ('Ava Turner', 808, 'Turner School of Entrepreneurship and Innovation', 'ava.turner@example.com'),
   ('Benjamin Carter', 909, 'Charley Steiner School of Sports Communication', 'benjamin.carter@example.com'),
   ('Mia Scott', 1010, 'Foster College of Business', 'mia.scott@example.com');      
''')

# # Create table - REGISTRATIONS
cursor.execute('''
CREATE TABLE IF NOT EXISTS registrations (
   student_id INTEGER,
   semester TEXT NOT NULL,
   course TEXT NOT NULL,
   instructor TEXT NOT NULL,
   FOREIGN KEY (student_id) REFERENCES students (student_id),
   FOREIGN KEY (semester) REFERENCES semesters (semester),
   FOREIGN KEY (course) REFERENCES courses (course_name),
   FOREIGN KEY (instructor) REFERENCES instructors (instructor_name)
)
''')

cursor.execute('''
INSERT INTO registrations (student_id, semester, course, instructor)
VALUES
   (123456, 'Spring 2023', 'CIS 475', 'Smith Johnson'),
   (987654, 'Summer 2023', 'CIS 430', 'Emma Johnson'),
   (456789, 'Fall 2023', 'BIO 292', 'Emily Davis'),
   (543210, 'Spring 2024', 'CHEM 101', 'Alex Martin'),
   (654321, 'Summer 2024', 'CS 140', 'Olivia Thompson'),
   (345678, 'Fall 2024', 'ENT 280', 'Daniel Harris'),
   (876543, 'Spring 2025', 'COM 103', 'Sophia Nelson'),
   (234567, 'Summer 2025', 'COM 292', 'Liam Lewis'),
   (789012, 'Fall 2025', 'CS 475', 'Ava Turner'),
   (678901, 'Spring 2026', 'MIS 173', 'Benjamin Carter');
''')



# Commit the changes
conn.commit()

# Close the connection
conn.close()
