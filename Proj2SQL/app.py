import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient
from bson.objectid import ObjectId
try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
    db = client["school_db"]
    collection = db["students"]
    client.server_info()
except Exception:
    messagebox.showerror("Error", "MongoDB Server is not running!")
    exit()
def add_student():
    name, age, dept = name_entry.get().strip(), age_entry.get().strip(), dept_entry.get().strip()
    if not all([name, age, dept]):
        messagebox.showwarning("Input Error", "All fields are required!")
        return
    collection.insert_one({"name": name, "age": age, "dept": dept})
    clear_fields()
    load_data()
def load_data():
    for i in tree.get_children(): tree.delete(i)
    for s in collection.find():
        tree.insert("", "end", values=(str(s["_id"]), s["name"], s["age"], s["dept"]))
    total_label.config(text=f"Total Students: {collection.count_documents({})}")
def delete_student():
    selected = tree.selection()
    if not selected: return
    if messagebox.askyesno("Confirm", "Delete this record?"):
        collection.delete_one({"_id": ObjectId(tree.item(selected[0])["values"][0])})
        load_data()
def clear_fields():
 for entry in [name_entry, age_entry, dept_entry]: entry.delete(0, tk.END)
root = tk.Tk()
root.title("Student Management System")
root.geometry("800x550")
style = ttk.Style()
style.configure("Treeview", rowheight=30)
style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
frame = tk.Frame(root, padx=20, pady=20)
frame.pack(fill="x")
tk.Label(frame, text="Name:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
name_entry = tk.Entry(frame, width=40)
name_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Label(frame, text="Age:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
age_entry = tk.Entry(frame, width=10)
age_entry.grid(row=0, column=3, padx=5, pady=5)
tk.Label(frame, text="Dept:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
dept_entry = tk.Entry(frame, width=40)
dept_entry.grid(row=1, column=1, padx=5, pady=5)
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="Add Student", command=add_student, bg="#4CAF50", fg="white", width=12).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Delete", command=delete_student, bg="#f44336", fg="white", width=12).pack(side=tk.LEFT, padx=5)
tree = ttk.Treeview(root, columns=("id", "name", "age", "dept"), show="headings")
tree.column("id", width=220, anchor="center") 
tree.column("name", width=150, anchor="center")
tree.column("age", width=50, anchor="center")
tree.column("dept", width=100, anchor="center")
tree.heading("id", text="Student ID (Hash)")
tree.heading("name", text="Name")
tree.heading("age", text="Age")
tree.heading("dept", text="Department")
tree.pack(pady=10, padx=20, fill="both", expand=True)
total_label = tk.Label(root, text="Total Students: 0", font=("Arial", 10, "bold"))
total_label.pack(pady=5)
load_data()
root.mainloop()