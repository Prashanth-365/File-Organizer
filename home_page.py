import winsound
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from separate_name import extract
import format_date
import os
import customtkinter
import pygame

file_extensions = {
    "IMG": [
        ".jpeg", ".jpg", ".png", ".gif", ".bmp", ".tiff",
        ".tif", ".svg", ".webp", ".heic", ".raw",
        ".cr2", ".nef", ".arw", ".orf", ".rw2", ".psd",
        ".eps"
    ],
    "VID": [
        ".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv",
        ".webm", ".m4v", ".vob", ".3gp", ".rmvb", ".ts",
        ".f4v", ".dv"
    ]
}
restricted_words = ['img', 'vid', 'image', 'video', 'pm']


class HomePage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("File Name Formatter")
        self.root.geometry("700x400")

        self.options = ["File Type", "Date", "Time", "Other Name", "App Name"]
        self.default_format = {
            "File Type": 'img',
            "Date": '2023-07-25',
            "Time": '17:05:46',
            "Other Name": 'Screenshot',
            "App Name": 'AdobeAcrobat'
        }

        self.dropdowns = []
        self.get_dropdowns = []
        self.file_name_format = []

        # Directory Input
        self.labels = tk.Frame(self.root)
        self.labels.grid(row=0, column=0, columnspan=3, sticky='ew')

        tk.Label(self.labels, text="Select Folder:").grid(row=0, column=0, sticky="w", padx=10)
        self.dir_entry = tk.Entry(self.labels, width=40)
        self.dir_entry.grid(row=0, column=1, padx=10)
        browse_button = tk.Button(self.labels, text="Browse", command=self.browse_directory)
        browse_button.grid(row=0, column=2, pady=30)

        # Format Blocks
        self.block_frame = tk.Frame(self.root)
        self.block_frame.grid(row=3, column=0, columnspan=3, pady=5, sticky='ew')

        # Initialize with default settings
        tk.Label(self.labels, text="Format:").grid(row=1, column=0, sticky="w", padx=10)
        self.set_default()

        # Add/Remove Section Buttons
        self.add_remove_frame = tk.Frame(self.root)
        self.add_remove_frame.grid(row=4, column=0, columnspan=3, sticky='ew')

        add_button = tk.Button(self.add_remove_frame, text="Add Section", command=self.add_section)
        remove_button = tk.Button(self.add_remove_frame, text="Remove Section", command=self.remove_section)
        reset_button = tk.Button(self.add_remove_frame, text="Reset to Default", command=self.reset_default)
        add_button.grid(row=0, column=0, padx=10)
        remove_button.grid(row=0, column=1, padx=10)
        reset_button.grid(row=0, column=2, pady=10)

        # Example Display
        self.example_label = tk.Label(self.labels, text='img_2023-07-25_17:05:46_Screenshot_AdobeAcrobat')
        self.example_label.grid(row=2, column=0, columnspan=3, sticky="ew", padx=10)

        self.checkbox_var = tk.BooleanVar()

        # Create a checkbox
        self.checkbox = tk.Checkbutton(self.root, text="Ask everytime if there is a change in date", variable=self.checkbox_var)
        self.checkbox.grid(row=5, column=1, pady=10)

        # Start Button
        start_button = tk.Button(self.root, text="Start Renaming", command=self.start_renaming)
        start_button.grid(row=6, column=1, pady=10)

        # Configure column weights to center the rows
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        self.root.mainloop()

    def browse_directory(self):
        directory = filedialog.askdirectory()
        self.dir_entry.delete(0, tk.END)
        self.dir_entry.insert(0, directory)

    def reset_default(self):
        for widget in self.block_frame.winfo_children():
            widget.destroy()
        self.dropdowns.clear()
        self.set_default()

    def set_default(self):
        for idx, option in enumerate(self.default_format):
            dropdown = ttk.Combobox(self.block_frame, values=self.options, width=12)
            dropdown.grid(row=1, column=idx, padx=2)
            dropdown.set(option)
            dropdown.bind("<<ComboboxSelected>>", self.update_example)
            self.dropdowns.append(dropdown)

        # SLNO Length
        # tk.Label(self.block_frame, text="SLNO Length:").grid(row=1, column=len(self.dropdowns), padx=10)
        # self.slno_spinbox = tk.Spinbox(self.block_frame, from_=1, to=5, width=5)
        # self.slno_spinbox.grid(row=1, column=len(self.dropdowns) + 1, padx=10)
        # self.slno_spinbox.bind("<KeyRelease>", self.update_example)
        # self.slno_spinbox.bind("<ButtonRelease>", self.update_example)

    def update_example(self, *args):
        self.get_dropdowns = [dropdown.get() for dropdown in self.dropdowns if dropdown.get()]
        example_format = "_".join([self.default_format[item] for item in self.get_dropdowns])
        # slno = "0" * int(self.slno_spinbox.get())
        self.example_label.config(text=f"{example_format}")
        # self.file_name_format = self.get_dropdowns + [slno]

    def start_renaming(self):
        self.update_example()
        directory = self.dir_entry.get()
        # messagebox.showinfo("Renaming", "Files are being renamed")
        ResultPage(self.root, directory, self.get_dropdowns, self.checkbox_var.get())

    def add_section(self):
        column = len(self.dropdowns)
        new_dropdown = ttk.Combobox(self.block_frame, values=self.options, width=12)
        new_dropdown.grid(row=1, column=column, padx=10)
        new_dropdown.set("Other Name")
        new_dropdown.bind("<<ComboboxSelected>>", self.update_example)

        self.dropdowns.append(new_dropdown)
        self.update_example()

    def remove_section(self):
        if len(self.dropdowns) > 1:
            last_dropdown = self.dropdowns.pop()
            last_dropdown.grid_forget()
            self.update_example()

    def show_result_page(self):
        pass


class ResultPage:
    def __init__(self, parent, directory, file_format, checkbox_status):
        self.rename = tk.Toplevel(parent)
        self.rename.title("Renaming Result")
        self.rename.geometry("400x200")

        tk.Label(self.rename, text="Renaming Result", font=("Helvetica", 16)).pack(pady=10)

        self.status_label = tk.Label(self.rename, text="Processing...", font=("Helvetica", 12))
        self.status_label.pack(pady=20)
        self.change_date_checkbox = checkbox_status
        self.file_name_format = file_format
        threading.Thread(target=self.format_file_name, args=(directory,)).start()

    def check_if_file_already_exists(self, file_name, directory):
        for file_path in Path(directory).rglob('*'):
            if file_path.is_file() and file_name == file_path.stem:
                return True
        return False

    import os

    def rename_file_with_slno(self, old_filename, formatted_filename, extension):
        slno = 0
        new_filename = formatted_filename + extension
        while True:
            try:
                if slno != 0:
                    new_filename = f"{formatted_filename}({slno}){extension}"
                # os.rename(old_filename, new_filename)
                print(f"File renamed to: {new_filename}")
                break
            except FileExistsError:
                slno += 1

    def format_file_name(self, directory):
        # try:
        count = 0
        for file_path in Path(directory).rglob('*'):
            if file_path.is_file():
                file_name = file_path.stem
                file_extension = file_path.suffix.lower()
                extracted_data = extract(file_name)
                date_modified = format_date.get_date_modified(file_path)
                extracted_date = None
                ignore_change = False
                if 'date_time' in extracted_data:
                    extracted_date = extracted_data['date_time']
                elif 'number' in extracted_data:
                    ignore_change = True
                    extracted_date = format_date.convert_from_timestamp(extracted_data['number'])

                change_date = format_date.modify_date(str(date_modified), str(extracted_date))
                if date_modified is not None or extracted_date is not None:
                    ignore_change = True
                elif date_modified[:12] == extracted_date[:12] and '00:00:00' not in extracted_date:
                    ignore_change = True

                if change_date:
                    extracted_data['date_time'] = date_modified
                    if self.change_date_checkbox and not ignore_change:
                        answer = messagebox.askyesno("Change Date", "Do you want to change the date?"
                                                                    f"\nFile Name : {file_name}"
                                                                    f"\n{extracted_date} -----> {date_modified}")
                        winsound.Beep(1000, 500)
                        if not answer:
                            extracted_data['date_time'] = extracted_date

                else:
                    extracted_data['date_time'] = extracted_date

                date_time = extracted_data.get('date_time', '00:00:00')
                if ' ' in date_time:
                    extracted_data['Date'], extracted_data['Time'] = date_time.split(' ', 1)
                    extracted_data['Time'] = extracted_data['Time'] .replace(":", "-")
                else:
                    extracted_data['Date'] = 'UnknownDate'
                    extracted_data['Time'] = 'UnknownTime'
                del extracted_data['date_time']

                formated_filename = ''
                for key in self.file_name_format:
                    if key == 'File Type':
                        for file_type, extensions in file_extensions.items():
                            if file_extension in extensions:
                                formated_filename += f'{file_type}_'
                                break
                    if key in extracted_data:
                        value = extracted_data[key]
                        if value.lower() not in restricted_words and value != '00:00:00':
                            formated_filename += f'{value.capitalize()}_'

                print(file_name + file_extension)
                self.rename_file_with_slno(file_name, formated_filename[:-1], file_extension)
                print()

                # Rename the file
                # new_file_path = file_path.with_name(new_filename)
                # file_path.rename(new_file_path)

                count += 1
                # Optionally update the status label
                # if count % 10 == 0:
                self.status_label.config(text=f"Renamed {count} files...")

        self.status_label.config(text=f"Renaming Complete! Total files renamed: {count}")
        # Optionally, close the window after some time
        self.rename.after(5000, self.rename.destroy)
        # except Exception as e:
        #     messagebox.showerror("Error", f"An error occurred: {e}")
        #     self.rename.destroy()


if __name__ == "__main__":
    HomePage()
