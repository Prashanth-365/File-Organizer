import customtkinter as ctk

# Initialize customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Create the main application window
app = ctk.CTk()
app.title("Table with Borders in customtkinter")
app.geometry("500x400")

# Define the number of rows and columns for the table
rows = 3
columns = 3

# Create a table with borders around each cell
for row in range(rows):
    for col in range(columns):
        # Create a frame to simulate cell borders
        cell_frame = ctk.CTkFrame(app, corner_radius=0, fg_color="gray")
        cell_frame.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")

        # Expand the cell to fill the available space
        app.grid_rowconfigure(row, weight=1)
        app.grid_columnconfigure(col, weight=1)

        if row == 0:
            # Create a label for the header row
            label = ctk.CTkLabel(cell_frame, text=f"Header {col + 1}")
            label.pack(expand=False, fill="both", padx=5, pady=5)
        else:
            # Create a button for other cells
            button = ctk.CTkButton(cell_frame, text=f"Button {row},{col}")
            button.pack(expand=False, fill="both", padx=5, pady=5)

# Start the application
app.mainloop()
