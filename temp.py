import os
import csv
import customtkinter as ctk
from tkinter import messagebox


class WorkoutTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Workout Exercise Tracker")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.exercise_rows = []

        self.create_main_window()

    def create_main_window(self):
        # Frame for exercise inputs
        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=10, padx=10, fill="x")

        # Dropdown for exercise selection
        self.exercise_var = ctk.StringVar(value="Select an exercise")
        self.dropdown = ctk.CTkComboBox(frame, variable=self.exercise_var,
                                        values=["Biceps Curls", "Push Ups", "Squats", "Lunges", "Plank"])
        self.dropdown.grid(row=0, column=0, padx=10, pady=5)

        # Sets and Reps entry
        self.sets_entry = ctk.CTkEntry(frame, placeholder_text="Sets", width=100)
        self.sets_entry.insert(0, "3")
        self.sets_entry.grid(row=0, column=1, padx=10, pady=5)

        self.reps_entry = ctk.CTkEntry(frame, placeholder_text="Reps", width=100)
        self.reps_entry.insert(0, "5")
        self.reps_entry.grid(row=0, column=2, padx=10, pady=5)

        # Buttons to add and remove rows
        add_button = ctk.CTkButton(frame, text="Add Row", command=self.add_row)
        add_button.grid(row=0, column=3, padx=10, pady=5)

        remove_button = ctk.CTkButton(frame, text="Remove Row", command=self.remove_row)
        remove_button.grid(row=0, column=4, padx=10, pady=5)

        # Frame for exercise rows
        self.rows_frame = ctk.CTkFrame(self.root)
        self.rows_frame.pack(pady=10, padx=10, fill="x")

        # Settings button
        settings_button = ctk.CTkButton(self.root, text="Settings", command=self.open_settings_window)
        settings_button.pack(pady=5)

    def add_row(self):
        exercise = self.exercise_var.get()
        sets = self.sets_entry.get()
        reps = self.reps_entry.get()

        if exercise == "Select an exercise" or not sets.isdigit() or not reps.isdigit():
            messagebox.showerror("Error", "Please select an exercise and enter valid sets and reps.")
            return

        row = ctk.CTkFrame(self.rows_frame)
        row.pack(pady=2)

        ctk.CTkLabel(row, text=exercise).pack(side="left", padx=10)
        ctk.CTkLabel(row, text=sets).pack(side="left", padx=10)
        ctk.CTkLabel(row, text=reps).pack(side="left", padx=10)

        self.exercise_rows.append({"Exercise": exercise, "Sets": sets, "Reps": reps})

    def remove_row(self):
        if self.rows_frame.winfo_children():
            row_to_remove = self.rows_frame.winfo_children()[-1]
            row_to_remove.destroy()
            self.exercise_rows.pop()

    def get_all_values(self):
        return self.exercise_rows

    def open_settings_window(self):
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("800x400")

        # Load settings data from CSV
        self.load_settings_data(settings_window)

    def load_settings_data(self, settings_window):
        frame = ctk.CTkFrame(settings_window)
        frame.pack(pady=10, padx=10, fill="both", expand=True)

        headers = ["Exercise Name", "Joint 1", "Joint 2", "Joint 3", "Actions"]
        for col_num, header in enumerate(headers):
            ctk.CTkLabel(frame, text=header, width=20).grid(row=0, column=col_num, padx=5, pady=5)

        # Load data from CSV file
        if os.path.exists("../workout_assistant/exercise_settings.csv"):
            with open("../workout_assistant/exercise_settings.csv", "r") as file:
                reader = csv.reader(file)
                for row_index, row in enumerate(reader, start=1):
                    exercise_name = row[0]
                    joint1 = row[1]
                    joint2 = row[2]
                    joint3 = row[3]

                    ctk.CTkLabel(frame, text=exercise_name).grid(row=row_index, column=0, padx=5, pady=5)
                    ctk.CTkLabel(frame, text=joint1).grid(row=row_index, column=1, padx=5, pady=5)
                    ctk.CTkLabel(frame, text=joint2).grid(row=row_index, column=2, padx=5, pady=5)
                    ctk.CTkLabel(frame, text=joint3).grid(row=row_index, column=3, padx=5, pady=5)

                    # Add Edit and Remove buttons
                    edit_button = ctk.CTkButton(frame, text="Edit", command=lambda r=row: self.edit_exercise(r))
                    edit_button.grid(row=row_index, column=4, padx=5, pady=5)

                    remove_button = ctk.CTkButton(frame, text="Remove", command=lambda r=row: self.remove_exercise(r))
                    remove_button.grid(row=row_index, column=5, padx=5, pady=5)

    def edit_exercise(self, existing_row):
        edit_window = ctk.CTkToplevel(self.root)
        edit_window.title("Edit Exercise")

        # Inputs for Exercise Name and Joints
        exercise_name = ctk.StringVar(value=existing_row[0])
        joint1 = ctk.StringVar(value=existing_row[1])
        joint2 = ctk.StringVar(value=existing_row[2])
        joint3 = ctk.StringVar(value=existing_row[3])

        ctk.CTkLabel(edit_window, text="Exercise Name").pack()
        name_entry = ctk.CTkEntry(edit_window, textvariable=exercise_name)
        name_entry.pack()

        # Inputs for joints and angles
        joint_entries = []
        for i, joint_var in enumerate([joint1, joint2, joint3], start=1):
            joint_frame = ctk.CTkFrame(edit_window)
            joint_frame.pack(pady=5)

            ctk.CTkLabel(joint_frame, text=f"Joint {i}").pack(side="left")
            entry = ctk.CTkEntry(joint_frame, textvariable=joint_var)
            entry.pack(side="left")
            joint_entries.append(entry)

        # Save and Cancel buttons
        save_button = ctk.CTkButton(edit_window, text="Save", command=lambda: self.save_exercise(edit_window, exercise_name, joint1, joint2, joint3, existing_row))
        save_button.pack(pady=10)

        cancel_button = ctk.CTkButton(edit_window, text="Cancel", command=edit_window.destroy)
        cancel_button.pack()

    def save_exercise(self, edit_window, exercise_name, joint1, joint2, joint3, existing_row):
        # Validate and save data to CSV
        new_data = [exercise_name.get(), joint1.get(), joint2.get(), joint3.get()]

        if not os.path.exists("../workout_assistant/exercise_settings.csv"):
            with open("../workout_assistant/exercise_settings.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(new_data)
        else:
            # Update existing data
            with open("../workout_assistant/exercise_settings.csv", "r") as file:
                rows = list(csv.reader(file))
            if existing_row:
                rows[rows.index(existing_row)] = new_data
            else:
                rows.append(new_data)

            with open("../workout_assistant/exercise_settings.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)
        edit_window.destroy()

        # Show success message
        messagebox.showinfo("Success", "Exercise saved successfully!")


if __name__ == "__main__":
    root = ctk.CTk()
    app = WorkoutTrackerApp(root)
    root.mainloop()
