import os
import re
import tkinter as tk
from tkinter import ttk, messagebox
import csv
import pandas as pd


class GUI:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("Simple Student Information System")
        self.app.geometry("1200x400")
        self.frame = ttk.Frame(self.app)  # Initialize frame after app
        self.treeview = None
        self.course_manager_window = None  # Keep track of the CourseManager window
        self.setup_widgets()

    def setup_widgets(self):
        self.frame.grid(sticky="nsew")
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.widgets_frame = ttk.LabelFrame(self.frame, text="Register here!")
        self.widgets_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        self.entry_name = tk.Entry(self.widgets_frame)
        self.entry_name.insert(0, "Name")
        self.entry_name.bind("<FocusIn>", lambda e: self.entry_name.delete('0', 'end'))
        self.entry_name.grid(row=0, column=0, sticky="ew", padx=5, pady=10)

        self.entry_idnum = tk.Entry(self.widgets_frame)
        self.entry_idnum.insert(0, "ID Number")
        self.entry_idnum.bind("<FocusIn>", lambda e: self.entry_idnum.delete('0', 'end'))
        self.entry_idnum.grid(row=1, column=0, sticky="ew", padx=5, pady=10)

        level = ["1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year", "6th Year"]
        self.entry_yrlvl = ttk.Combobox(self.widgets_frame, values=level)
        self.entry_yrlvl.insert("0", "Year Level")
        self.entry_yrlvl.grid(row=2, column=0, sticky="ew", padx=5, pady=10)

        gender_list = ["Male", "Female", "Other"]
        self.entry_gender = ttk.Combobox(self.widgets_frame, values=gender_list)
        self.entry_gender.insert("0", "Gender")
        self.entry_gender.grid(row=3, column=0, sticky="ew", padx=5, pady=10)

        courseCode_list = Course.read_course_codes_from_csv('course.csv', course_code_list=None)
        self.entry_courseCode = ttk.Combobox(self.widgets_frame, values=courseCode_list)
        self.entry_courseCode.insert("0", "Course")
        self.entry_courseCode.grid(row=4, column=0, sticky="ew", padx=5, pady=5)

        self.button_submit = tk.Button(self.widgets_frame, text="SUBMIT", command=self.on_button_submit)
        self.button_submit.grid(row=6, column=0, padx=5, pady=5)

        self.seperator = ttk.Separator(self.widgets_frame)
        self.seperator.grid(row=7, column=0, sticky="ew", padx=(20, 10), pady=5)

        self.treeFrame = ttk.Frame(self.frame)
        self.treeFrame.grid(row=0, column=1, pady=10, sticky="nsew")
        self.treeFrame.columnconfigure(0, weight=1)
        self.treeFrame.rowconfigure(0, weight=1)

        self.button_frame1 = ttk.Frame(self.treeFrame)
        self.button_frame1.pack(side="bottom", pady=10, anchor="e")

        self.button_edit = tk.Button(self.button_frame1, text="EDIT", command=self.on_button_edit)
        self.button_edit.pack(side="left", padx=5)

        self.button_del = tk.Button(self.button_frame1, text="DELETE", command=self.on_button_del)
        self.button_del.pack(side="left", padx=5)

        self.button_load = tk.Button(self.button_frame1, text="LOAD", command=self.on_button_load)
        self.button_load.pack(side="right", padx=5)

        self.button_manage = tk.Button(self.button_frame1, text="COURSES", command=self.on_button_courses)
        self.button_manage.pack(side="right", padx=5)

        self.search_frame = ttk.Frame(self.treeFrame)
        self.search_frame.pack(side="top", pady=10, anchor="e")

        self.entry_search = tk.Entry(self.search_frame)
        self.entry_search.insert(0, "Search Name or ID")
        self.entry_search.bind("<FocusIn>", lambda e: self.entry_search.delete('0', 'end'))
        self.entry_search.pack(side="left", padx=5)

        self.button_search = tk.Button(self.search_frame, text="SEARCH", command=self.search_student)
        self.button_search.pack(side="left", padx=5)

        self.button_save = tk.Button(self.widgets_frame, text="SAVE", command=self.on_button_save)

        self.treeScroll = ttk.Scrollbar(self.treeFrame)
        self.treeScroll.pack(side="right", fill="y")

        # Define the column names
        cols = ["Name", "ID_Number", "Year_Level", "Gender", "Course_Code", "Course_Title", "Status"]

        # Create the Treeview widget
        self.treeview = ttk.Treeview(self.treeFrame, show="headings", yscrollcommand=self.treeScroll.set, columns=cols,
                                     height=13)

        # Set up headings
        for col in cols:
            self.treeview.heading(col, text=col)

        # Set up columns
        for col in cols:
            self.treeview.column(col, width=200, anchor="center")

        self.treeview.column("Name", width=200, anchor="center")
        self.treeview.column("ID_Number", width=100, anchor="center")
        self.treeview.column("Year_Level", width=80, anchor="center")
        self.treeview.column("Gender", width=80, anchor="center")
        self.treeview.column("Course_Code", width=100, anchor="center")
        self.treeview.column("Course_Title", width=300, anchor="center")
        self.treeview.column("Status", width=100, anchor="center")

        self.treeview.pack(expand=True, fill="both")
        self.treeScroll.config(command=self.treeview.yview)

    def on_button_submit(self):
        name = self.entry_name.get()
        id_num = self.entry_idnum.get()
        yr_lvl = self.entry_yrlvl.get()
        gender = self.entry_gender.get()
        course_code = self.entry_courseCode.get()

        # Validate the ID number using the Student class method
        if not Student.validate_id_number(id_num):
            messagebox.showerror("Error", "Invalid ID number format. Please enter in the format: YYYY-NNNN")
            return

        if name == "Name" or id_num == "ID Number" or yr_lvl == "Year Level" or gender == "Gender" or course_code == "Course":
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if not (name and id_num and yr_lvl and gender and course_code):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        existing_ids = Student.load_student_ids('student.csv')
        if Student.check_duplicate_id(id_num, existing_ids):
            messagebox.showerror("Error", "Invalid ID number. Already existing ID number.")
            return

        # Append the user input to the CSV file
        with open('student.csv', mode='a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([name, id_num, yr_lvl, gender, course_code])

        # Update student status
        Student.update_student_status()

        # Refresh Treeview
        self.on_button_load()

        # Clear entry widgets
        self.entry_name.delete(0, tk.END)
        self.entry_idnum.delete(0, tk.END)
        self.entry_yrlvl.delete(0, tk.END)
        self.entry_gender.delete(0, tk.END)
        self.entry_courseCode.delete(0, tk.END)

        # Make the guides appear
        self.entry_name.insert(0, "Name")
        self.entry_idnum.insert(0, "ID Number")
        self.entry_yrlvl.insert(0, "Year Level")
        self.entry_gender.insert(0, "Gender")
        self.entry_courseCode.insert(0, "Course Code")

        messagebox.showinfo("Success", "Information added successfully.")

    def on_button_edit(self):
        # Get the selected item in the treeview
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a row to edit.")
            return

        # Get the values of the selected row
        values = self.treeview.item(selected_item)['values']

        # Populate the registration segment fields with the selected values
        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, values[0])

        self.entry_idnum.delete(0, tk.END)
        self.entry_idnum.insert(0, values[1])

        self.entry_yrlvl.delete(0, tk.END)
        self.entry_yrlvl.insert(0, values[2])

        self.entry_gender.delete(0, tk.END)
        self.entry_gender.insert(0, values[3])

        self.entry_courseCode.delete(0, tk.END)
        self.entry_courseCode.insert(0, values[4])

        # This removes the submit button to be replaced by the save button
        self.button_submit.grid_remove()

        self.button_save.grid(row=6, column=0, padx=5, pady=5)
        messagebox.showinfo("Editing", "You are now editing.")
        pass

    def on_button_del(self):
        # Get the selected item in the treeview
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a row to delete.")
            return

        # Ask for confirmation before deleting
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this row?")

        if confirmation:
            # Get the unique identifier of the selected row (e.g., ID number)
            selected_row_id = self.treeview.item(selected_item)['values'][1]

            # Delete the selected row from the CSV file
            with open("student.csv", mode="r", newline='') as csvfile:
                reader = csv.reader(csvfile)
                rows = [row for row in reader if row[1] != selected_row_id]  # Exclude the selected row

            # Write the updated rows back to the CSV file
            with open("student.csv", mode="w", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(rows)

            # Delete the selected row from the Treeview
            self.treeview.delete(selected_item)

            # Update student status
            Student.update_student_status()
            root.on_button_load()
            messagebox.showinfo("Deleting", "Information deleted successfully.")
        pass

    def on_button_load(self):
        if os.path.exists("student.csv"):
            df = pd.read_csv("student.csv")

            # Clear existing items in the Treeview
            for item in self.treeview.get_children():
                self.treeview.delete(item)

            # Load courses
            course_codes = Course.read_course_codes_from_csv('course.csv', course_code_list=None)
            courses = Course.load_courses('course.csv')

            # Insert data into the Treeview with center alignment
            for index, row in df.iterrows():
                course_code = row['Course_Code']
                if course_code not in courses:
                    course_code = "N/A"  # Display "N/A" if course code not found
                course_title = courses.get(course_code, "Unknown")  # Get course title or "Unknown" if not found
                status = "Enrolled" if course_title != "Unknown" else "Unenrolled"  # Set status based on course existence

                self.treeview.insert("", "end", values=(
                    row["Name"], row["ID_Number"], row["Year_Level"], row["Gender"], course_code, course_title, status),
                                     tags="centered")

            # Set a tag for centered alignment
            self.treeview.tag_configure("centered", anchor="center")

    def on_button_courses(self):
        # Instantiate CourseManager GUI with self.app as its parent
        course_manager_window = tk.Toplevel(self.app)
        course_manager_window.title("Course Manager")
        # Create CourseManager instance with course_manager_window as parent
        course_manager = CourseManager(course_manager_window)

    def search_student(self):
        query = self.entry_search.get().strip().lower()  # Get the search query and convert it to lowercase

        if not query:
            return  # If the search query is empty, do nothing

        # Iterate through the data in the CSV file and search for the query
        for row_id in self.treeview.get_children():
            row = self.treeview.item(row_id)['values']
            if query in row[0].lower() or query in row[1].lower():  # Check if the query matches name or ID number
                self.treeview.selection_set(row_id)  # Select the row in the treeview
                self.treeview.focus(row_id)  # Focus on the selected row
                self.treeview.see(row_id)  # Scroll to make the selected row visible
                return  # Stop searching after the first match

        self.entry_search.delete(0, tk.END)
        self.entry_search.insert(0, "Search Name or ID")

    def on_button_save(self):
        # Get the selected item in the treeview
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a row to save.")
            return

        # Get the values of the selected row
        name = self.entry_name.get()
        id_num = self.entry_idnum.get()
        yr_lvl = self.entry_yrlvl.get()
        gender = self.entry_gender.get()
        course_code = self.entry_courseCode.get()

        # Check if any field is empty
        if not (name and id_num and yr_lvl and gender and course_code):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Validate ID number format
        if not Student.validate_id_number(id_num):
            messagebox.showerror("Error",
                                 "Invalid ID number format. Please enter a valid ID number in the format 'YYYY-NNNN'.")
            return

        # Get the index of the selected row
        selected_row_index = self.treeview.index(selected_item)

        # Exclude the ID of the selected student being edited from the duplication check
        existing_ids = Student.load_student_ids('student.csv')
        selected_student_id = self.treeview.item(selected_item)['values'][1]
        if selected_student_id in existing_ids:
            existing_ids.remove(selected_student_id)

        # Check for duplicate ID
        if Student.check_duplicate_id(id_num, existing_ids, selected_student_id):
            messagebox.showerror("Error",
                                 "Invalid ID number. Already existing ID number.")
            return

        # Update the values in the CSV file
        with open("student.csv", mode="r", newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            if len(rows) > selected_row_index + 1:  # Check if the selected row index is within bounds
                rows[selected_row_index + 1] = [name, id_num, yr_lvl, gender,
                                                course_code]  # Update the values in the corresponding row
            else:
                messagebox.showerror("Error", "Selected row index is out of bounds.")
                return

        with open("student.csv", mode="w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)

        # Update the Treeview with the edited values
        self.treeview.item(selected_item, values=(name, id_num, yr_lvl, gender, course_code))

        # Update student status
        Student.update_student_status()

        # Clear entry widgets
        self.entry_name.delete(0, tk.END)
        self.entry_idnum.delete(0, tk.END)
        self.entry_yrlvl.delete(0, tk.END)
        self.entry_gender.delete(0, tk.END)
        self.entry_courseCode.delete(0, tk.END)

        self.button_save.grid_remove()
        self.button_submit.grid(row=6, column=0, padx=5, pady=5)

        Student.update_student_status()
        root.on_button_load()

        messagebox.showinfo("Success", "Information edited successfully.")

    pass

    def run(self):
        self.app.mainloop()


class Student:
    @staticmethod
    def validate_id_number(id_num):
        if id_num is None:
            return False  # Return False if id_num is None
        pattern = r'^\d{4}-\d{4}$'  # Regex pattern for YEAR-number format
        return bool(re.match(pattern, id_num))

    @staticmethod
    def check_duplicate_id(id_num, student_ids, excluded_id=None):
        if excluded_id:
            student_ids = student_ids - {excluded_id}
        return id_num in student_ids

    @staticmethod
    def update_student_status():
        # Read student data from CSV
        df = pd.read_csv("student.csv")
        courses = Course.load_courses('course.csv')
        statuses = []

        # Update statuses for each student
        for index, row in df.iterrows():
            course_code = row['Course_Code']
            if course_code == "None":
                statuses.append("Unenrolled")  # If course code is "None", status is "Unenrolled"
            elif course_code in courses:
                statuses.append("Enrolled")  # If course is found in the courses, status is "Enrolled"
            else:
                statuses.append("Unenrolled")  # Otherwise, status is "Unenrolled"

        # Update status column in DataFrame
        df['Status'] = statuses

        # Write updated DataFrame back to CSV
        df.to_csv("student.csv", index=False)

    @staticmethod
    def load_student_ids(filename):
        student_ids = set()
        try:
            with open(filename, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header
                for row in reader:
                    student_ids.add(row[1])  # Assuming ID_Number is in the second column
        except FileNotFoundError:
            print(f"Error: {filename} not found.")
        except Exception as e:
            print(f"Error: {e}")
        return student_ids


class Course:
    @staticmethod
    def get_course_title(code):
        courses = Course.load_courses('course.csv')
        return courses.get(code.strip().upper(), "Unknown")

    @staticmethod
    def check_course(course_code, courses):
        if isinstance(course_code, float):
            # Convert course_code to string if it's a float
            course_code = str(course_code)
        return course_code.upper() in courses

    @staticmethod
    def load_courses(filename):
        courses = {}  # Initialize an empty dictionary to store course information
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) == 2:
                    code, name = row
                    courses[code.strip()] = name.strip()
        return courses

    @staticmethod
    def read_course_codes_from_csv(filename, course_code_list):
        if course_code_list is None:
            course_code_list = []

        try:
            with open(filename, mode="r", newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row:
                        course_info = row[0].split(",")  # Split the row by comma
                        if len(course_info) >= 1:
                            course_code = course_info[0].strip().upper()  # Get the course code
                            if course_code not in course_code_list:
                                course_code_list.append(course_code)
        except FileNotFoundError:
            print(f"Error: {filename} not found.")
        except Exception as e:
            print(f"Error: {e}")

        return course_code_list


class CourseManager:
    def __init__(self, parent):
        # Initialize the GUI and other attributes
        self.parent = parent
        self.parent.geometry("580x300")  # Increase the window size
        self.setup_widgets()
        self.create_csv_file_if_not_exists()

    def setup_widgets(self):
        # Create widgets for CourseManager GUI
        self.course_frame = ttk.LabelFrame(self.parent, text="Manage Courses")
        self.course_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.entry_course_code = ttk.Entry(self.course_frame)
        self.entry_course_code.insert(0, "Course Code")
        self.entry_course_code.bind("<FocusIn>", lambda e: self.entry_course_code.delete('0', 'end'))
        self.entry_course_code.grid(row=0, column=0, padx=5, pady=5)

        self.entry_course_title = ttk.Entry(self.course_frame)
        self.entry_course_title.insert(0, "Course Title")
        self.entry_course_title.bind("<FocusIn>", lambda e: self.entry_course_title.delete('0', 'end'))
        self.entry_course_title.grid(row=0, column=1, padx=5, pady=5)

        self.button_add_course = ttk.Button(self.course_frame, text="Add Course", command=self.add_course)
        self.button_add_course.grid(row=0, column=2, padx=5, pady=5)

        self.button_edit_course = ttk.Button(self.course_frame, text="Edit Course", command=self.edit_course)
        self.button_edit_course.grid(row=0, column=3, padx=5, pady=5)

        self.button_delete_course = ttk.Button(self.course_frame, text="Delete Course", command=self.delete_course)
        self.button_delete_course.grid(row=0, column=4, padx=5, pady=5)

        # Create a Treeview widget
        self.course_tree = ttk.Treeview(self.course_frame, columns=("Course Code", "Course Title"), selectmode="browse")

        # Add columns to the Treeview
        self.course_tree.heading("#0", text="", anchor="w")
        self.course_tree.heading("Course Code", text="Course Code")
        self.course_tree.heading("Course Title", text="Course Title")

        self.course_tree.column("#0", width=0, stretch=tk.NO)
        self.course_tree.column("Course Code", width=100)
        self.course_tree.column("Course Title", width=400)

        self.course_tree.grid(row=1, column=0, columnspan=5, padx=5, pady=5)

        self.load_course_list()

    def create_csv_file_if_not_exists(self):
        with open("course.csv", "a+") as file:
            pass

    def add_course(self):
        course_code = self.entry_course_code.get().strip().upper()
        course_title = self.entry_course_title.get().strip()

        # Check if the entry fields still contain the placeholder strings
        if course_code == "Course Code" or course_title == "Course Title":
            messagebox.showerror("Error", "Please enter both course code and title.")
            return

        # Validate inputs
        if not course_code or not course_title:
            messagebox.showerror("Error", "Please enter both course code and title.")
            return

        # Check for duplicate course code
        if self.check_duplicate_course_code(course_code):
            messagebox.showerror("Error", "Course code already exists.")
            return

        # Add the new course to the CSV file
        with open("course.csv", "a", encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([course_code, course_title])

        # Clear entry widgets
        self.entry_course_code.delete(0, tk.END)
        self.entry_course_title.delete(0, tk.END)
        self.entry_course_code.insert(0, "Course Code")
        self.entry_course_title.insert(0, "Course Title")

        # Update course list
        self.load_course_list()

        messagebox.showinfo("Success", "Course added successfully.")

    def delete_course(self):
        selected_item = self.course_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a course to delete.")
            return

        # Get the selected course code from the Treeview
        course_code = self.course_tree.item(selected_item, "values")[0]

        confirmation = messagebox.askyesno("Confirmation", f"Are you sure you want to delete {course_code}?")
        if not confirmation:
            return

        # Remove the selected course from the Treeview
        self.course_tree.delete(selected_item)

        # Read all courses from the CSV file into memory
        courses = []
        with open("course.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] != course_code:  # Exclude the line corresponding to the deleted course
                    courses.append(row)

        # Rewrite the CSV file with the updated course list
        with open("course.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerows(courses)

        messagebox.showinfo("Success", "Course deleted successfully.")

    def edit_course(self):
        selected_item = self.course_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a course to edit.")
            return

        # Get the selected course details from the Treeview
        course_code, course_title = self.course_tree.item(selected_item, "values")

        # Populate the entry widgets with the selected course details for editing
        self.entry_course_code.delete(0, tk.END)
        self.entry_course_code.insert(0, course_code)
        self.entry_course_title.delete(0, tk.END)
        self.entry_course_title.insert(0, course_title)

        # Disable the delete and add buttons
        self.button_delete_course.config(state="disabled")
        self.button_add_course.config(state="disabled")

        # Replace the edit button with a save button
        self.button_edit_course.grid_remove()  # Remove the edit button
        self.button_save_course = ttk.Button(self.course_frame, text="Save Course Changes",
                                             command=self.save_course_changes)
        self.button_save_course.grid(row=0, column=3, padx=5, pady=5)

    def save_course_changes(self):
        selected_item = self.course_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a course to save changes.")
            return

        # Get the selected course details from the Treeview
        course_code = self.entry_course_code.get().strip().upper()
        course_title = self.entry_course_title.get().strip()

        # Check for duplicate course code
        if course_code != self.course_tree.item(selected_item, "values")[0] and self.check_duplicate_course_code(
                course_code):
            messagebox.showerror("Error", "Course code already exists.")
            return

        # Update the selected course details in the Treeview
        self.course_tree.item(selected_item, values=(course_code, course_title))

        # Update the course details in the CSV file
        courses = []
        for item in self.course_tree.get_children():
            values = self.course_tree.item(item, "values")
            courses.append(values)

        with open("course.csv", "w", newline="") as file:
            writer = csv.writer(file)
            for course in courses:
                writer.writerow(course)

        # Return button to original state
        self.button_save_course.grid_remove()
        self.button_edit_course.grid(row=0, column=3, padx=5, pady=5)
        self.button_delete_course.config(state="normal")
        self.button_add_course.config(state="normal")

        self.load_course_list()

        messagebox.showinfo("Success", "Changes saved successfully.")

    def check_duplicate_course_code(self, course_code):
        # Check if the entered course code already exists in the CSV file
        with open("course.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == course_code:
                    return True
        return False

    def load_course_list(self):
        # Clear current course list in Treeview
        self.course_tree.delete(*self.course_tree.get_children())

        # Load courses from the CSV file and populate Treeview
        with open("course.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                self.course_tree.insert("", tk.END, values=row)


if __name__ == "__main__":
    root = GUI()
    root.run()
