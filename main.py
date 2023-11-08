import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# Create the main window
root = tk.Tk()
root.title("Course Management System")

# Create frames for organizing widgets
top_frame = tk.Frame(root)
top_frame.pack(pady=10, padx=10, fill='x')

middle_frame = tk.Frame(root)
middle_frame.pack(pady=10, padx=10, fill='x')

bottom_frame = tk.Frame(root)
bottom_frame.pack(pady=10, padx=10, fill='x')

# Add a frame for updating semester information
update_frame = tk.Frame(root)
update_frame.pack(pady=10, padx=10, fill='x')

course_id_combobox_label = tk.Label(middle_frame, text="Select Course ID:")
course_id_combobox_label.grid(row=1, column=0, sticky='e')
course_id_combobox = ttk.Combobox(middle_frame, state="readonly")  # Create a read-only Combobox
course_id_combobox.grid(row=1, column=1)

def populate_course_id_combobox():
    # Connect to the database
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    # Get all course IDs
    cursor.execute('SELECT course_id FROM courses')
    course_ids = cursor.fetchall()

    # Update the combobox's values with the list of course IDs
    course_id_combobox['values'] = [str(course_id[0]) for course_id in course_ids]

    # If there are courses, set the current selection to the first course ID
    if course_ids:
        course_id_combobox.current(0)

    conn.close()

# Create the course_id_combobox widget
course_id_combobox = ttk.Combobox(middle_frame, state="readonly")
course_id_combobox.grid(row=1, column=1)

# Function to update course_id_combobox values
def update_course_id_combobox_values():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('SELECT course_id FROM courses')
    course_ids = cursor.fetchall()
    populate_course_id_combobox['values'] = [str(course_id[0]) for course_id in course_ids]
    if course_ids:
        populate_course_id_combobox.current(0)
    conn.close()

# Call this function to initially populate the combobox and also after adding a new course
populate_course_id_combobox()

update_course_name_label = tk.Label(update_frame, text="New Course Name:")
update_course_name_label.grid(row=1, column=0, sticky='e')
update_course_name_entry = tk.Entry(update_frame)
update_course_name_entry.grid(row=1, column=1, padx=5, pady=5)

course_entry_label = tk.Label(top_frame, text="Enter course name:")
course_entry_label.grid(row=1, column=0, sticky='e')
course_entry = tk.Entry(top_frame)
course_entry.grid(row=1, column=1)

semester_entry_label = tk.Label(top_frame, text="Enter semester information:")
semester_entry_label.grid(row=2, column=0, sticky='e')
semester_entry = tk.Entry(top_frame)
semester_entry.grid(row=2, column=1)

student_entry_label = tk.Label(middle_frame, text="Enter student name:")
student_entry_label.grid(row=0, column=0, sticky='e')
student_entry = tk.Entry(middle_frame)
student_entry.grid(row=0, column=1)

student_course_id_entry_label = tk.Label(middle_frame, text="Enter Course ID:")
student_course_id_entry_label.grid(row=1, column=0, sticky='e')
student_course_id_entry = tk.Entry(middle_frame)
student_course_id_entry.grid(row=1, column=1)

course_list_label = tk.Label(bottom_frame, text="Courses:")
course_list_label.pack()
course_list = tk.Listbox(bottom_frame)
course_list.pack(fill='x')

def add_course():
    # Retrieve values from the GUI input fields
    course_name = course_entry.get()
    semester = semester_entry.get()  # Assuming you have an input field for the semester

    # Connect to the database and insert the new course
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    
    # Insert a new course
    cursor.execute('''
    INSERT INTO courses(course_name, semester)
    VALUES(?, ?)
    ''', (course_name, semester))
    
    # Show a message box as feedback
    messagebox.showinfo("Add Course", f"Course {course_name} added successfully for {semester} semester.")

    # Clear the input fields
    course_entry.delete(0, tk.END)
    semester_entry.delete(0, tk.END)

    # Update the course list display
    display_courses()

    # Update the combobox with new course IDs
    populate_course_id_combobox()

    conn.commit()
    conn.close()

def register_student():
    # Retrieve student name from the Entry widget
    student_name = student_entry.get()
    # Retrieve selected course ID from the Combobox widget
    course_id = course_id_combobox.get()

    # Input validation
    if not student_name or not course_id:
        messagebox.showwarning("Warning", "Please enter both student name and select a course ID.")
        return
    
    # Connect to the database and register the student
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    # Check if the course exists (already selected from the combobox, so this check is optional)
    cursor.execute('SELECT * FROM courses WHERE course_id = ?', (course_id,))
    if not cursor.fetchone():
        messagebox.showwarning("Warning", "The selected course ID does not exist.")
        conn.close()
        return
    
    # Insert a new student registration
    try:
        cursor.execute('''
        INSERT INTO students(student_name, course_id)
        VALUES(?, ?)
        ''', (student_name, course_id))
    except sqlite3.IntegrityError as e:
        # This will occur if the course_id doesn't exist or if there's a duplicate entry
        messagebox.showerror("Error", f"Failed to register student: {e}")
    else:
        conn.commit()
        messagebox.showinfo("Register Student", f"Student {student_name} registered to course ID {course_id} successfully.")
    
    # Clear the input fields
    student_entry.delete(0, tk.END)
    course_id_combobox.set('')  # Clear the combobox selection
    
    conn.close()


def delete_course():
    # Check if a course is selected
    selected_items = course_list.curselection()
    if not selected_items:
        messagebox.showwarning("Warning", "Please select a course to delete.")
        return

    # Get the selected item
    selected_item = course_list.get(selected_items[0])
    course_id = selected_item.split(" - ")[0]  # Assuming the course_id is the first part of the string

    # Confirm deletion with the user
    if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete course {course_id}?"):
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()
        
        # Execute the delete operation
        cursor.execute('DELETE FROM courses WHERE course_id = ?', (course_id,))
        conn.commit()
        conn.close()

        # Update the course list display
        display_courses()

        # Update the combobox with new course IDs
        populate_course_id_combobox()

        messagebox.showinfo("Delete Course", f"Course {course_id} deleted successfully.")


def update_semester(course_id, new_semester):
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    
    cursor.execute('UPDATE courses SET semester = ? WHERE course_id = ?', (new_semester, course_id))
    conn.commit()

    # Show a message box as feedback
    messagebox.showinfo("Update Semester", f"Semester updated successfully for course ID {course_id}.")

    conn.close()

def update_course():
    # Get the index of the selected course in the Listbox
    selected_indices = course_list.curselection()
    if not selected_indices:
        messagebox.showwarning("Update Course", "Please select a course to update.")
        return
    
    # Get the selected course's text
    selected_course = course_list.get(selected_indices[0])
    # Extract the course ID from the selected course text
    course_id = selected_course.split(" - ")[0]

    # Get the new course name from the Entry widget
    new_name = update_course_name_entry.get()
    if not new_name:
        messagebox.showwarning("Update Course", "Please enter the new course name.")
        return

    # Update the course name in the database using the extracted course ID
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE courses SET course_name = ? WHERE course_id = ?', (new_name, course_id))
    conn.commit()
    conn.close()

    # Show a message box as feedback
    messagebox.showinfo("Update Course", f"Course ID {course_id} updated successfully to {new_name}.")

    # Clear the update entry field
    update_course_name_entry.delete(0, tk.END)

    # Refresh the course list display
    display_courses()



def display_courses():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT course_id, course_name, semester FROM courses')
    courses = cursor.fetchall()

    # Clear the current list
    course_list.delete(0, tk.END)

    # Insert the new list of courses
    for course in courses:
        course_list.insert(tk.END, f"{course[0]} - {course[1]} - {course[2]}")
    
    conn.close()


# Add buttons to top frame
add_course_button = tk.Button(top_frame, text="Add Course", command=add_course)
add_course_button.grid(row=3, column=1, sticky='e', pady=5)

# Add buttons to middle frame
register_student_button = tk.Button(middle_frame, text="Register Student", command=register_student)
register_student_button.grid(row=2, column=1, sticky='e', pady=5)

# Add buttons to bottom frame
delete_course_button = tk.Button(bottom_frame, text="Delete Course", command=delete_course)
delete_course_button.pack(side='left', padx=5)
# Add button to update the course name
update_course_button = tk.Button(update_frame, text="Update Course", command=update_course)
update_course_button.grid(row=2, column=1, sticky='e', padx=5, pady=5)


display_courses_button = tk.Button(bottom_frame, text="Display Courses", command=display_courses)
display_courses_button.pack(side='left', padx=5)

# Start the main loop
root.mainloop()
