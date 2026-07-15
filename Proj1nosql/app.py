from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["studentdb"]
collection = db["students"]
def line():
    print("=" * 50)
while True:
    line()
    print("STUDENT MANAGEMENT SYSTEM")
    line()
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Total Students")
    print("7. Delete All Students")
    print("8. Exit")
    choice = input("\nEnter Choice: ")
    # ---------------- ADD ----------------
    if choice == "1":
        name = input("Name: ")
        age = input("Age: ")
        department = input("Department: ")
        collection.insert_one({
            "name": name,
            "age": age,
            "department": department
        })
        print("\nStudent Added Successfully!")
    # ---------------- VIEW ----------------
    elif choice == "2":
        students = list(collection.find())
        if len(students) == 0:
            print("\nNo Student Found.")
        else:
            print("\n")
            print("{:<20} {:<8} {:<15}".format("NAME", "AGE", "DEPARTMENT"))
            print("-" * 45)
            for s in students:
                print("{:<20} {:<8} {:<15}".format(
                    s.get("name", ""),
                    s.get("age", ""),
                    s.get("department", "")
                ))
    # ---------------- SEARCH ----------------
    elif choice == "3":
        name = input("Enter Student Name: ")
        student = collection.find_one({"name": name})
        if student:
            print("\nStudent Found")
            print("Name :", student.get("name"))
            print("Age :", student.get("age"))
            print("Department :", student.get("department"))
        else:
            print("Student Not Found!")
    # ---------------- UPDATE ----------------
    elif choice == "4":
        old_name = input("Student Name: ")
        student = collection.find_one({"name": old_name})
        if student:
            new_name = input("New Name: ")
            new_age = input("New Age: ")
            new_department = input("New Department: ")
            collection.update_one(
                {"name": old_name},
                {
                    "$set": {
                        "name": new_name,
                        "age": new_age,
                        "department": new_department
                    }
                }
            )
            print("Updated Successfully!")
        else:
            print("Student Not Found!")

    # ---------------- DELETE ----------------
    elif choice == "5":
        name = input("Student Name: ")
        result = collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print("Deleted Successfully!")
        else:
            print("Student Not Found!")

    # ---------------- COUNT ----------------
    elif choice == "6":

        total = collection.count_documents({})
        print("\nTotal Students =", total)

    # ---------------- DELETE ALL ----------------
    elif choice == "7":
        confirm = input("Delete All Students? (yes/no): ")

        if confirm.lower() == "yes":
            collection.delete_many({})
            print("All Students Deleted.")

    # ---------------- EXIT ----------------
    elif choice == "8":
        print("\nThank You.")
        break
    else:
        print("Invalid Choice!")