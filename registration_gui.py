import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class StudentRoster:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Course Management System")

        self.student_info = []
        self.course_infos = []
        self.course_descs = []

    def run(self):
        self.view_students()
        self.root.mainloop()    

    def validate_entries(self, entries):
        for entry in entries:
            if entry.get() == entry.placeholder:
                return False

        try:
            student_id = int(entries[0].get())
            student_first = entries[1].get()
            student_last = entries[2].get()
            student_major = entries[3].get()
            student_gpa = float(entries[4].get())
        except ValueError:
            return False

        return True
    
    def is_student_id_exists(self, student_id):
        connection = sqlite3.connect('registration.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        result = cursor.fetchone()

        connection.close()

        return result is not None
    
    def is_course_exists(self, course):
        connection = sqlite3.connect('registration.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM courses WHERE course_name = ?", (course,))
        result = cursor.fetchone()

        connection.close()

        return result is not None
    
    def is_instructor_exists(self, instructor):
        connection = sqlite3.connect('registration.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM course WHERE course = ?", (instructor,))
        result = cursor.fetchone()

        connection.close()

        return result is not None
    
    def add_student_to_db(self, entries, top, tree=None):
        if self.validate_entries(entries):
            try:
                student_id = int(entries[0].get())
                student_first = entries[1].get()
                student_last = entries[2].get()
                student_major = entries[3].get()
                student_gpa = float(entries[4].get())

                if self.is_student_id_exists(student_id):
                    tk.messagebox.showerror("Error", "Student ID already exists in the database.")

                    entries[0].delete(0, tk.END)
                    entries[0].insert(0, entries[0].placeholder) 
                    
                    return

                connection = sqlite3.connect('registration.db')
                cursor = connection.cursor()

                cursor.execute("INSERT INTO students (student_id, firstname, lastname, major, gpa) VALUES (?, ?, ?, ?, ?)",
                            (student_id, student_first, student_last, student_major, student_gpa))

                connection.commit()
                connection.close()

                top.destroy()

                if tree:
                    self.populate_student_list(tree)

            except ValueError:
                tk.messagebox.showerror("Error", "Invalid data types. Please enter valid values.")

                if int(entries[0].get()):
                    entries[0].delete(0, tk.END)
                    entries[0].insert(0, entries[0].placeholder) 
                elif float(entries[4].get()):
                    entries[4].delete(0, tk.END)
                    entries[4].insert(0, entries[4].placeholder) 
        else:
            tk.messagebox.showerror("Error", "All entries must be filled, and data types must be valid.")

    def add_students(self, frame, tree=None, student_id=None):
        add_student_entries = []
        top = tk.Toplevel(frame)
        top.grab_set()

        title = tk.Label(top, text="Add a student", justify=tk.CENTER)
        title.pack()

        def on_entry_click(event, entry):
            if entry.get() == entry.placeholder:
                entry.delete(0, "end")
                entry.config(fg="black")

        placeholders = ["Student ID", "Student Firstname", "Student Lastname", "Student Major", "Student GPA"]
        for placeholder_text in placeholders:
            if student_id and placeholder_text == "Student ID":
                entry = tk.Entry(top, fg="black")
                entry.insert(0, student_id)
                entry.config(state='readonly')
            else:
                entry = tk.Entry(top, fg="black")
                entry.insert(0, placeholder_text)
                entry.placeholder = placeholder_text

            entry.bind("<FocusIn>", lambda event, entry=entry: on_entry_click(event, entry))
            entry.bind("<FocusOut>", lambda event, entry=entry: on_focus_out(event, entry))
            entry.pack(pady=5, padx=10)
            add_student_entries.append(entry)

        def on_focus_out(event, entry):
            if entry.get() == "":
                entry.insert(0, entry.placeholder)
                entry.config(fg="black")

                if entry.get() == entry.placeholder:
                    return
                else:
                    add_student_entries[:] = [e.get() for e in add_student_entries]
        
        if tree:
            back_button = tk.Button(top, text='Ok', width=10, command=lambda: self.add_student_to_db(add_student_entries, top, tree=tree))
        else:
            back_button = tk.Button(top, text='Ok', width=10, command=lambda: self.add_student_to_db(add_student_entries, top))
        back_button.pack(pady=5, padx=10)

        cancel_button = tk.Button(top, text='CANCEL', width=10, command=lambda: top.destroy())
        cancel_button.pack(pady=5, padx=10)
    
    def edit_courses(self, frame, course_list, view_course=False):
        edit_window = tk.Toplevel(frame)
        edit_window.grab_set()

        title = tk.Label(edit_window, text="Edit Course Info", justify=tk.CENTER)
        title.grid(row=0, columnspan=2, padx=5, pady=5)

        labels = ['Course Name', 'Course Location', 'Course Description', 'Course Hours']
        entry_vars_list = []

        for i, course in enumerate(course_list):
            if i == 0:
                tk.Label(edit_window, text=labels[i]).grid(row=i+1, column=0, padx=5, pady=5)
                
                entry_var = tk.StringVar(value=course)
                tk.Entry(edit_window, textvariable=entry_var, state="readonly").grid(row=i+1, column=1, padx=5, pady=5)
            else:
                tk.Label(edit_window, text=labels[i]).grid(row=i+1, column=0, padx=5, pady=5)
                
                entry_var = tk.StringVar(value=course)
                tk.Entry(edit_window, textvariable=entry_var).grid(row=i+1, column=1, padx=5, pady=5)
                entry_vars_list.append(entry_var)

        def update_course_info():
            updated_values = [entry_var.get() for entry_var in entry_vars_list]
            updated_values.insert(0, course_list[0])

            connection = sqlite3.connect('registration.db')
            cursor = connection.cursor()

            update_query = "UPDATE courses SET course_name=?, location=?, description=?, hours=? WHERE course_name=?"
            cursor.execute(update_query, (*updated_values, course_list[0]))

            connection.commit()
            connection.close()

            edit_window.destroy()

            if view_course:
                self.view_courses(reg_list=updated_values, frame=frame)

        tk.Button(edit_window, text='Apply Changes', command=update_course_info).grid(row=len(course_list)*len(labels)+1, columnspan=2, pady=5)
        tk.Button(edit_window, text='Cancel', command=lambda: edit_window.destroy()).grid(row=len(course_list)*len(labels)+2, columnspan=2, pady=5)

    def delete_student(self, student_list):
        student_id = self.get_selected_primary(student_list)

        if student_id is not None:
            confirmation = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this student?")
            
            if confirmation:
                try:
                    connection = sqlite3.connect('registration.db')
                    cursor = connection.cursor()

                    cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))

                    connection.commit()

                    connection.close()

                    self.populate_student_list(student_list)

                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Error deleting student: {e}")

            else:
                messagebox.showinfo("Deletion Cancelled", "Student deletion has been cancelled.")
        else:
            messagebox.showinfo("No Student Selected", "Please select a student to delete.")

    def edit_student(self, frame, student_list):
        selected_item = student_list.selection()
        
        if not selected_item:
            self.show_warning_popup("No Student Selected", "Please select a student to edit.")
            return

        values = student_list.item(selected_item, 'values')

        edit_window = tk.Toplevel(frame)
        edit_window.grab_set()

        title = tk.Label(edit_window, text="Edit Student Info", justify=tk.CENTER)
        title.grid(row=0,columnspan=2, padx=5, pady=5)

        labels = ['Student ID', 'First Name', 'Last Name', 'Major', 'GPA']
        entry_vars = []

        for i, label in enumerate(labels):
            if i == 0:
                tk.Label(edit_window, text=label).grid(row=i+1, column=0, padx=5, pady=5)
                entry_var = tk.StringVar(value=values[i])
                tk.Entry(edit_window, textvariable=entry_var, state='readonly').grid(row=i+1, column=1, padx=5, pady=5)
            else:
                tk.Label(edit_window, text=label).grid(row=i+1, column=0, padx=5, pady=5)
                entry_var = tk.StringVar(value=values[i])
                tk.Entry(edit_window, textvariable=entry_var).grid(row=i+1, column=1, padx=5, pady=5)
                entry_vars.append(entry_var)

        def update_student_info():
            updated_values = [entry_var.get() for entry_var in entry_vars]

            student_list.item(selected_item, values=(values[0], *updated_values))

            connection = sqlite3.connect('registration.db')
            cursor = connection.cursor()

            update_query = "UPDATE students SET firstname=?, lastname=?, major=?, gpa=? WHERE student_id=?"
            cursor.execute(update_query, (*updated_values, values[0]))

            connection.commit()
            connection.close()

            edit_window.destroy()

        tk.Button(edit_window, text='Apply Changes', command=update_student_info).grid(row=len(labels)+1, columnspan=2, pady=5)
        tk.Button(edit_window, text='Cancel', command=lambda: edit_window.destroy()).grid(row=len(labels)+2, columnspan=2, pady=5)

    def show_warning_popup(self, title, message):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        tk.Label(popup, text=message, padx=10, pady=10).pack()
        tk.Button(popup, text="OK", command=popup.destroy).pack()

    def view_students(self, frame=None):
        if frame:
            frame.pack_forget()

        student_frame = tk.LabelFrame(self.root, text='STUDENTS ELIGIBLE')
        student_frame.pack(pady=10, padx=10, fill='x')

        columns = ('Student ID', 'First Name', 'Last Name', 'Major', 'GPA')
        student_list = ttk.Treeview(student_frame, columns=columns, show='headings', selectmode='browse')
        for col in columns:
            student_list.heading(col, text=col)
            student_list.column(col, width=120)
        student_list.pack(fill='x', side='left', padx=5)
        self.populate_student_list(student_list)

        add_button = tk.Button(student_frame, text='ADD', width=10, command=lambda: self.add_students(student_frame, student_list))
        add_button.pack(pady=5, padx=10, anchor='s')

        delete_button = tk.Button(student_frame, text='DELETE', width=10, command=lambda: self.delete_student(student_list))
        delete_button.pack(pady=5, padx=10, anchor='s')

        edit_button = tk.Button(student_frame, text='EDIT', width=10, command=lambda: self.edit_student(student_frame, student_list))
        edit_button.pack(pady=5, padx=10, anchor='s')

        view_button = tk.Button(student_frame, text='VIEW', width=10, command=lambda: self.view_classes(id=self.get_selected_primary(student_list), frame=student_frame))
        view_button.pack(pady=5, padx=10, anchor='s')

    def populate_student_list(self, student_list):
        student_list.delete(*student_list.get_children())

        empty_label = getattr(self, "_empty_student_label", None)
        if empty_label:
            empty_label.destroy()

        connection = sqlite3.connect('registration.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM students WHERE gpa >= 2.00")
        rows = cursor.fetchall()

        for row in rows:
            student_list.insert('', 'end', values=row)

        if not rows:
            empty_label = tk.Label(student_list, text="No Eligible Students Found", font=("Arial", 12), background='white')
            empty_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

            self._empty_student_label=empty_label
        connection.close()

    def get_selected_primary(self, list, index=0):
        selected_item = list.selection()
        if selected_item:
            student_id = list.item(selected_item)['values'][index]
            return student_id
        return None

    def cleanup_classes(self, e, frame):
        self.student_info = []
        for entry in e:
            self.student_info.append(entry.get())
        frame.destroy()

    def register_student(self, frame, entries, ids=None):
        connection = sqlite3.connect('registration.db')
        cursor = connection.cursor()

        if ids:
            print(ids)
            student_id = ids
        else:
            student_id = entries[0].get()
        semester = entries[1].get()
        course_name = entries[2].get()
        instructor = entries[3].get()

        cursor.execute("SELECT * FROM registrations WHERE student_id = ? AND semester = ? AND course = ? AND instructor = ?", (student_id, semester, course_name, instructor))
        existing_registration = cursor.fetchone()

        if existing_registration:
            tk.messagebox.showwarning("Registration Warning", "Student is already registered for this course.")
        else:
            cursor.execute("INSERT INTO registrations (student_id, semester, course, instructor) VALUES (?, ?, ?, ?)",
                        (student_id, semester, course_name, instructor))

            connection.commit()
            connection.close()

            if ids:
                self.view_classes(id=ids, frame=frame)
            else:
                self.view_classes(frame=frame)

    def register_classes(self, frame, tree, students=None):
        if frame:
            frame.pack_forget()

        register_class_entries = []
        id = None

        register_class = tk.LabelFrame(self.root, text='COURSE SELECTION')
        register_class.pack(pady=10, padx=10, fill='x')

        student_label = tk.Label(register_class, text="Student ID:")
        student_label.grid(row=0, column=0, sticky='e')
        selected_item = tree.selection()
        if students.get() != "All Students":
            student_id = tree.item(selected_item, 'values')
            student = students.get()
            student_option = tk.Entry(register_class, text=student)
            student_option.grid(row=0, column=1, pady=5, padx=10)
            student_option.delete(0, tk.END)
            student_option.insert(0, student)
            student_option.config(state='readonly')
            student_var = tk.StringVar()
            student_var.set(student)
            id = students.get()
            register_class_entries.append(student_var)
        elif selected_item:
            student_id = tree.item(selected_item, 'values')
            student = ''.join(map(str, student_id[0]))
            student_option = tk.Entry(register_class, text=student)
            student_option.grid(row=0, column=1, pady=5, padx=10)
            student_option.delete(0, tk.END)
            student_option.insert(0, student)
            student_option.config(state='readonly')
            student_var = tk.StringVar()
            student_var.set(student)
            id = None
            register_class_entries.append(student_var)
        else:
            student = self.get_student_ids()
            student_var = tk.StringVar()
            student_var.set(student[0])
            student_option = tk.OptionMenu(register_class, student_var, *student)
            student_option.config(width=14)
            student_option.grid(row=0, column=1, pady=5, padx=10)
            id = None
            register_class_entries.append(student_var)

        semester_label = tk.Label(register_class, text="Semester:")
        semester_label.grid(row=1, column=0, sticky='e')
        semesters = self.get_semesters()
        semesters_var = tk.StringVar()
        semesters_var.set(semesters[0])
        semester_options = tk.OptionMenu(register_class, semesters_var, *semesters)
        semester_options.config(width=14)
        semester_options.grid(row=1, column=1, pady=5, padx=10)
        register_class_entries.append(semesters_var)

        course_label = tk.Label(register_class, text="Course:")
        course_label.grid(row=2, column=0, sticky='e')
        course = self.get_courses()
        course_var = tk.StringVar()
        course_var.set(course[0])
        course_options = tk.OptionMenu(register_class, course_var, *course)
        course_options.config(width=14)
        course_options.grid(row=2, column=1, pady=5, padx=10)
        register_class_entries.append(course_var)

        instructor_label = tk.Label(register_class, text="Instructor:")
        instructor_label.grid(row=3, column=0, sticky='e')
        instructor = self.get_instructors()
        instructor_var = tk.StringVar()
        instructor_var.set(instructor[0])
        instructor_options = tk.OptionMenu(register_class, instructor_var, *instructor)
        instructor_options.config(width=14)
        instructor_options.grid(row=3, column=1, pady=5, padx=10)
        register_class_entries.append(instructor_var)

        enter_button = tk.Button(register_class, text='REGISTER', width=10, command=lambda: self.register_student(register_class, register_class_entries, ids=id))
        enter_button.grid(row=4, columnspan=2, pady=2, padx=10)

        cancel_button = tk.Button(register_class, text='CANCEL', width=10, command=lambda: self.cleanup_register(register_class, ids=id))
        cancel_button.grid(row=5, columnspan=2, pady=3, padx=10)
    
    def cleanup_register(self, frame, ids=None):
        if ids:
            self.view_classes(frame=frame, id=ids)
        else:
            self.view_classes(frame=frame) 

    def populate_class_list(self, list_box, id=None, student_id_list=None):
        list_box.delete(*list_box.get_children())

        empty_label = getattr(self, "_empty_class_label", None)
        if empty_label:
            empty_label.destroy()

        connection = sqlite3.connect('registration.db')
        cursor = connection.cursor()

        rows = []
        if id:
            cursor.execute("SELECT * FROM registrations WHERE student_id = ?", (id,))
            rows = cursor.fetchall()
        elif student_id_list:
            for ids in student_id_list:
                cursor.execute("SELECT * FROM registrations WHERE student_id = ?", (ids,))
                rows.extend(cursor.fetchall())
        else:
            cursor.execute("SELECT * FROM registrations")
            rows = cursor.fetchall()

        for row in rows:
            list_box.insert('', 'end', values=row)

        if not rows:
            empty_label = tk.Label(list_box, text="Student is not enrolled in any classes", font=("Arial", 12), background='white')
            empty_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

            self._empty_class_label=empty_label

        connection.close()

    def get_student_ids(self):
        connection = sqlite3.connect('registration.db')
        cursor = connection.cursor()

        cursor.execute("SELECT student_id FROM students WHERE gpa >= 2.00")
        students = [int(student[0]) for student in cursor.fetchall()]

        connection.close()

        return students
    
    def get_course_info(self, course_name):
        self.course_descs = []

        connection = sqlite3.connect('registration.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM courses WHERE course_name = ?", (course_name,))

        course_info = cursor.fetchone()

        if course_info:
            self.course_descs.extend(course_info)

        connection.close()
    
    def get_semesters(self):
        connection = sqlite3.connect('registration.db')
        cursor = connection.cursor()

        cursor.execute("SELECT semester FROM semesters")
        semesters = [str(semester[0]) for semester in cursor.fetchall()]

        connection.close()

        return semesters
    
    def get_courses(self):
        connection = sqlite3.connect('registration.db')
        cursor = connection.cursor()

        cursor.execute("SELECT course_name FROM courses")
        courses = [str(course[0]) for course in cursor.fetchall()]

        connection.close()

        return courses
    
    def get_instructors(self):
        connection = sqlite3.connect('registration.db')
        cursor = connection.cursor()

        cursor.execute("SELECT instructor_name FROM instructors")
        instructors = [str(instructor[0]) for instructor in cursor.fetchall()]

        connection.close()

        return instructors
    
    def view_classes(self, id=None, frame=None):
        if frame:
            frame.pack_forget()

        classes_frame = tk.LabelFrame(self.root, text='STUDENTS CLASSES')
        classes_frame.pack(pady=10, padx=10, fill='x')

        columns = ('Student ID', 'Semester', 'Course', 'Instructor')
        course_list = ttk.Treeview(classes_frame, columns=columns, show='headings', selectmode='browse')
        for col in columns:
            course_list.heading(col, text=col)
            course_list.column(col, width=120)
        course_list.pack(fill='x', padx=5, pady=5)

        students = self.get_student_ids()
        students.insert(0, "All Students")
        
        student_var = tk.StringVar()
        if id:
            student_var.set(id)
            self.populate_class_list(course_list, id=id)
        else:
            student_var.set(students[0])
            students_id_list = self.get_student_ids()
            self.populate_class_list(course_list, student_id_list=students_id_list)

        student_id_options = tk.OptionMenu(classes_frame, student_var, *students)
        student_id_options.config(width=20)
        student_id_options.pack(side='left', padx=5)

        def view_classes_action(*args):
            selected_student_id = student_var.get()
            if selected_student_id == "All Students":
                students_id_list = self.get_student_ids()
                self.populate_class_list(course_list, student_id_list=students_id_list)
            else:
                self.populate_class_list(course_list, (int(selected_student_id)))

        select_button = tk.Button(classes_frame, text="SELECT STUDENT", command=view_classes_action)
        select_button.pack(side='left', pady=5)

        buttons_frame = tk.Frame(classes_frame)
        buttons_frame.pack(fill='x', padx=5, pady=5, side='bottom')

        register_button = tk.Button(buttons_frame, text='REGISTER COURSE', width=15, command=lambda: self.register_classes(classes_frame, course_list, students=student_var))
        register_button.pack(pady=5, padx=10)

        drop_button = tk.Button(buttons_frame, text='DROP COURSE', width=15, command=lambda: self.drop_course(course_list))
        drop_button.pack(pady=5, padx=10)

        view_button = tk.Button(buttons_frame, text='VIEW COURSE', width=15, command=lambda: self.view_courses(tree_list=course_list, frame=classes_frame))
        view_button.pack(pady=5, padx=10)

        back_button = tk.Button(buttons_frame, text='GO BACK', width=15, command=lambda: self.view_students(frame=classes_frame))
        back_button.pack(pady=5, padx=10)

    def drop_course(self, course_list):
        selected_item = course_list.selection()
        
        if not selected_item:
            tk.messagebox.showerror("Error", "Please select a course to drop.")
            return

        values = course_list.item(selected_item, 'values')

        student_id, semester, course_name, instructor = values

        connection = sqlite3.connect('registration.db')
        cursor = connection.cursor()

        delete_query = "DELETE FROM registrations WHERE student_id=? AND semester=? AND course=? AND instructor=?"
        cursor.execute(delete_query, (student_id, semester, course_name, instructor))

        connection.commit()
        connection.close()

        self.populate_class_list(course_list, student_id)

    def cleanup_edit(self, e, frame):
        self.course_descs = []
        for entry in e:
            self.course_descs.append(entry.get())
        frame.destroy()

    def view_courses(self, tree_list=None, reg_list=None, frame=None):
        if tree_list:
            if not self.get_selected_primary(tree_list):
                tk.messagebox.showerror("Error", "Please select a row to view course from table")
                return
        
        if frame:
            frame.pack_forget()

        course_frame = tk.LabelFrame(self.root, text='COURSE INFORMATION')
        course_frame.pack(pady=10, padx=10, fill='x')

        info_frame = tk.Frame(course_frame, background='white')
        info_frame.grid(row=0, columnspan=2, padx=5, pady=5)

        self.course_infos = ['Course Name', 'Course Location', 'Course Description', 'Course Hours']
        
        if tree_list:
            self.get_course_info(self.get_selected_primary(tree_list, index=2))
        else:
            self.course_descs = []
            for course in reg_list:
                self.course_descs.append(course)

        for index in range(0, 4):
            course_info = tk.Label(info_frame, text=self.course_infos[index] + ': ', background='white')
            course_info.grid(row=index, column=0, sticky='e')
            
            course_desc = tk.Label(info_frame, text=self.course_descs[index], background='white')
            course_desc.grid(row=index, column=1, sticky='w', padx=5)

        course_list = []
        [course_list.append(x) for x in self.course_descs]
        edit_button = tk.Button(course_frame, text='EDIT COURSE', width=15, command=lambda: self.edit_courses(course_frame, self.course_descs, view_course=True))
        edit_button.grid(row=len(self.course_infos)+1, columnspan=2, padx=10, pady=3)

        back_button = tk.Button(course_frame, text='GO BACK', width=15, command=lambda: self.view_classes(frame=course_frame))
        back_button.grid(row=len(self.course_infos)+2, columnspan=2, padx=10, pady=5)

if __name__ == '__main__':
    roster = StudentRoster()
    roster.run()
