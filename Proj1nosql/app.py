import customtkinter as ctk
from tkinter import ttk, messagebox
from pymongo import MongoClient
client=MongoClient("mongodb://localhost:27017/")
db=client["studentdb"]
collection=db["students"]
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Student Management System - Professional")
        self.geometry("900x700")
        self.style=ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", 
                             background="#2b2b2b", 
                             foreground="white", 
                             fieldbackground="#2b2b2b", 
                             borderwidth=0,
                             rowheight=30)
        self.style.configure("Treeview.Heading", 
                             background="#3b3b3b", 
                             foreground="white", 
                             relief="flat")
        self.style.map("Treeview",background=[('selected', '#1f538d')])
        self.label=ctk.CTkLabel(self,text="Student Management System",font=("Arial", 28, "bold"))
        self.label.pack(pady=15)
        self.input_frame=ctk.CTkFrame(self)
        self.input_frame.pack(pady=10,padx=20,fill="x")
        self.input_frame.grid_columnconfigure(1,weight=1)
        ctk.CTkLabel(self.input_frame, text="Name").grid(row=0, column=0, padx=15,pady=15,sticky="w")
        self.name_entry = ctk.CTkEntry(self.input_frame)
        self.name_entry.grid(row=0, column=1, padx=15, pady=15,sticky="ew")
        ctk.CTkLabel(self.input_frame, text="Age").grid(row=1,column=0, padx=15,pady=15,sticky="w")
        self.age_entry=ctk.CTkEntry(self.input_frame)
        self.age_entry.grid(row=1,column=1,padx=15,pady=15,sticky="ew")
        ctk.CTkLabel(self.input_frame,text="Department").grid(row=2, column=0,padx=15,pady=15,sticky="w")
        self.dept_entry = ctk.CTkEntry(self.input_frame)
        self.dept_entry.grid(row=2, column=1,padx=15,pady=15,sticky="ew")
        self.btn_frame = ctk.CTkFrame(self,fg_color="transparent")
        self.btn_frame.pack(pady=15)
        btns = [("Add", self.add_student), ("Search", self.search_student), 
                ("Update", self.update_student), ("Delete", self.delete_student),("Clear",self.clear_fields)]
        for text, cmd in btns:
            ctk.CTkButton(self.btn_frame, text=text, width=120, command=cmd).pack(side="left",padx=8)
        self.count_label = ctk.CTkLabel(self, text="Total Students: 0", font=("Arial", 14))
        self.count_label.pack()
        self.tree = ttk.Treeview(self,columns=("Name","Age","Dept"), show="headings",height=10)
        self.tree.heading("Name",text="Name")
        self.tree.heading("Age",text="Age")
        self.tree.heading("Dept",text="Department")
        self.tree.column("Name",width=250, anchor="center")
        self.tree.column("Age",width=120, anchor="center")
        self.tree.column("Dept",width=250, anchor="center")
        self.tree.pack(fill="both",expand=True,padx=20,pady=20)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.show_students()
    def update_counter(self):
        count = collection.count_documents({})
        self.count_label.configure(text=f"Total Students: {count}")
    def on_tree_select(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, 'values')
            self.clear_fields()
            self.name_entry.insert(0,values[0])
            self.age_entry.insert(0,values[1])
            self.dept_entry.insert(0,values[2])
    def show_students(self):
        for i in self.tree.get_children():self.tree.delete(i)
        for s in collection.find():
            self.tree.insert("", "end",values=(s.get("name"),s.get("age"),s.get("department")))
        self.update_counter()
    def add_student(self):
        collection.insert_one({"name":self.name_entry.get(),"age":self.age_entry.get(),"department":self.dept_entry.get()})
        self.show_students(); self.clear_fields()
    def search_student(self):
        s = collection.find_one({"name":self.name_entry.get()})
        if s:
            self.age_entry.delete(0,'end'); self.age_entry.insert(0,s["age"])
            self.dept_entry.delete(0,'end'); self.dept_entry.insert(0,s["department"])
        else: messagebox.showerror("Error","Not Found")
    def update_student(self):
        collection.update_one({"name":self.name_entry.get()}, {"$set":{"age":self.age_entry.get(),"department":self.dept_entry.get()}})
        self.show_students()
    def delete_student(self):
        collection.delete_one({"name":self.name_entry.get()})
        self.show_students();self.clear_fields()
    def clear_fields(self):
        self.name_entry.delete(0,'end');self.age_entry.delete(0,'end'); self.dept_entry.delete(0,'end')
if __name__ == "__main__":
    app = App()
    app.mainloop()
