import sqlite3
from tkinter import *
from tkinter import messagebox, ttk


# Database setup
def connect_db():
    conn = sqlite3.connect("blood_bank.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            blood_group TEXT NOT NULL,
            contact TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# Add donor to the database
def add_donor():
    if name_var.get() == "" or age_var.get() == "" or blood_group_var.get() == "" or contact_var.get() == "":
        messagebox.showwarning("Input Error", "All fields are required")
    else:
        conn = sqlite3.connect("blood_bank.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO donors (name, age, blood_group, contact) VALUES (?, ?, ?, ?)",
                       (name_var.get(), age_var.get(), blood_group_var.get(), contact_var.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Donor added successfully!")
        clear_fields()


# View all donors
def view_donors():
    conn = sqlite3.connect("blood_bank.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donors")
    rows = cursor.fetchall()
    for row in rows:
        donor_table.insert("", "end", values=row)
    conn.close()


# Search donors by blood group
def search_donors():
    donor_table.delete(*donor_table.get_children())
    conn = sqlite3.connect("blood_bank.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donors WHERE blood_group=?", (search_var.get(),))
    rows = cursor.fetchall()
    for row in rows:
        donor_table.insert("", "end", values=row)
    conn.close()


# Clear input fields
def clear_fields():
    name_var.set("")
    age_var.set("")
    blood_group_var.set("")
    contact_var.set("")


# GUI setup
connect_db()
root = Tk()
root.title("Blood Bank Management System")
root.geometry("700x500")

# Variables
name_var = StringVar()
age_var = StringVar()
blood_group_var = StringVar()
contact_var = StringVar()
search_var = StringVar()

# Widgets
Label(root, text="Blood Bank Management System", font=("Arial", 20)).pack(pady=10)

frame = Frame(root)
frame.pack(pady=20)

Label(frame, text="Name:").grid(row=0, column=0, padx=10, pady=5)
Entry(frame, textvariable=name_var).grid(row=0, column=1, padx=10, pady=5)

Label(frame, text="Age:").grid(row=1, column=0, padx=10, pady=5)
Entry(frame, textvariable=age_var).grid(row=1, column=1, padx=10, pady=5)

Label(frame, text="Blood Group:").grid(row=2, column=0, padx=10, pady=5)
Entry(frame, textvariable=blood_group_var).grid(row=2, column=1, padx=10, pady=5)

Label(frame, text="Contact:").grid(row=3, column=0, padx=10, pady=5)
Entry(frame, textvariable=contact_var).grid(row=3, column=1, padx=10, pady=5)

Button(frame, text="Add Donor", command=add_donor).grid(row=4, column=0, columnspan=2, pady=10)

Label(root, text="Search by Blood Group:").pack(pady=5)
Entry(root, textvariable=search_var).pack(pady=5)
Button(root, text="Search", command=search_donors).pack(pady=5)

columns = ("ID", "Name", "Age", "Blood Group", "Contact")
donor_table = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    donor_table.heading(col, text=col)
    donor_table.column(col, width=100)
donor_table.pack(pady=10)

Button(root, text="View All Donors", command=view_donors).pack(pady=5)

root.mainloop()