import customtkinter as ctk
from tkinter import messagebox
import json
import os


class HostelApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Hostel Bed Allocation System")
        self.geometry("650x700")
        self.file_path = "hostel_beds_data.json"

        self.beds = self.load_data()
        # Sort bed IDs (R1 B1d, R1 B1u...) for the dropdown list
        self.bed_options = sorted(self.beds.keys())

        # UI
        self.label = ctk.CTkLabel(
            self, text="Hostel Bed Allocation", font=("Arial", 22, "bold")
        )
        self.label.pack(pady=20)

        # Input(Name)
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Student Name", width=300)
        self.name_entry.pack(pady=10)

        # Input(Index no)
        self.index_entry = ctk.CTkEntry(
            self, placeholder_text="Index Number (ex. 23FISXXXX)", width=300
        )
        self.index_entry.pack(pady=10)

        # Bed Selection dropdown
        self.bed_label = ctk.CTkLabel(self, text="Select Bed ID:", font=("Arial", 13))
        self.bed_label.pack(pady=(10, 0))

        self.bed_dropdown = ctk.CTkOptionMenu(
            self, values=self.bed_options, width=300, dynamic_resizing=False
        )
        self.bed_dropdown.pack(pady=15)

        # Buttons
        self.assign_button = ctk.CTkButton(
            self, text="ADD", fg_color="green", command=self.allocate
        )
        self.assign_button.pack(pady=10)

        self.remove_button = ctk.CTkButton(
            self, text="REMOVE", fg_color="red", command=self.remove_student
        )
        self.remove_button.pack(pady=5)

        # Status Display
        self.status_box = ctk.CTkTextbox(
            self, width=500, height=350, font=("Courier New", 15)
        )
        self.status_box.pack(pady=20)
        self.update_display()

    def generate_empty_beds(self):
        """Creates the initial structure: 4 rooms, 2 bunks (Up/Down) each."""
        beds = {}
        for r in range(1, 5):  # Rooms 1-4
            for b in range(1, 3):  # Bunks 1-2
                for p in [" upper", " lower"]:
                    beds[f"Room{r} Bed{b}{p}"] = None
        return beds

    def load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                return json.load(file)
        return self.generate_empty_beds()

    def save_data(self):
        with open(self.file_path, "w") as file:
            json.dump(self.beds, file, indent=4)

    def update_display(self):
        self.status_box.delete("0.0", "end")
        header = f"{'rooms & beds':<20} || {'Name':<14} || {'indexno'}\n"
        self.status_box.insert("end", header)
        self.status_box.insert("end", " " * len(header) + "\n")

        for bed_id in self.bed_options:
            data = self.beds[bed_id]
            if data:
                line = f"{bed_id:<20} | {data['name']:<15} | {data['index']}\n\n"
            else:
                line = f"{bed_id:<20} | {'Available':<15} | {'-'}\n\n"
            self.status_box.insert("end", line)

    def allocate(self):
        name = self.name_entry.get().strip()
        idx = self.index_entry.get().strip()
        bed_id = self.bed_dropdown.get()  # Get selection from dropdown

        if self.beds[bed_id] is None:
            if name and idx:
                self.beds[bed_id] = {"name": name, "index": idx}
                self.save_data()
                self.update_display()
                messagebox.showinfo("Success", f"Allocated {bed_id} to {name}")
                self.name_entry.delete(0, "end")
                self.index_entry.delete(0, "end")
        else:
            messagebox.showerror("Occupied", "This bed is occupied")

    def remove_student(self):
        bed_id = self.bed_dropdown.get()
        if self.beds[bed_id] is not None:
            self.beds[bed_id] = None
            self.save_data()
            self.update_display()
            messagebox.showinfo("Success", "Bed is now available.")
        else:
            messagebox.showwarning("Status", "This bed is empty.")


if __name__ == "__main__":
    app = HostelApp()
    app.mainloop()
