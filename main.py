import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from pymongo import MongoClient, errors
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

mongo_connected = False
MONGODB_URI = os.getenv("MONGODB_URI")

if MONGODB_URI:
    try:
        db_client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        db_client.admin.command('ping')
        db = db_client['intellib']
        book_issue_collection = db['book_issue']
        student_record_collection = db['student_record']
        mongo_connected = True
    except (errors.ServerSelectionTimeoutError, errors.ConnectionFailure, errors.ConfigurationError):
        print("Warning: Could not connect to MongoDB. Running in offline mode.")
else:
    print("Warning: No MongoDB URI provided. Running in offline mode.")

manual_enrollment_number = None
scanned_barcode = None
detected_enrollment_number = None

def set_style():
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TFrame', background='#23272A')
    style.configure('TLabel', background='#2C2F33', foreground='white', font=('Helvetica', 14))
    style.configure('TEntry', fieldbackground='#23272A', foreground='white', font=('Helvetica', 14))
    style.configure('TButton', font=('Helvetica', 14), foreground='white', padding=10, relief='flat')
    style.map('TButton', background=[('!active', '#7289DA'), ('active', '#5B6EAE')], relief=[('active', 'flat')])

class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()

        set_style()
        self.title("IntelliLib - Intelligent Library")
        self.geometry("700x500")
        self.configure(bg='#2C2F33')

        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill='both', expand=True)

        self.label_title = ttk.Label(main_frame, text="📚 Welcome to IntelliLib", font=("Helvetica", 24, "bold"), foreground='#7289DA')
        self.label_title.pack(pady=20)

        self.label_enrollment = ttk.Label(main_frame, text="Enter Enrollment Number:", font=("Helvetica", 16))
        self.label_enrollment.pack(pady=10)

        self.entry_enrollment = ttk.Entry(main_frame, width=30, font=("Helvetica", 14))
        self.entry_enrollment.pack(pady=10)

        self.button_frame = ttk.Frame(main_frame)
        self.button_frame.pack(pady=20)

        self.button_check_books = ttk.Button(self.button_frame, text="📖 Check Books Issued", command=self.check_books_issued)
        self.button_check_books.grid(row=0, column=0, padx=10, pady=10)

        self.button_check_deadlines = ttk.Button(self.button_frame, text="⏳ Check Deadlines", command=self.check_deadlines)
        self.button_check_deadlines.grid(row=0, column=1, padx=10, pady=10)

        self.button_check_fine = ttk.Button(self.button_frame, text="💸 Check Fine", command=self.check_fine)
        self.button_check_fine.grid(row=1, column=0, padx=10, pady=10)

        self.button_issue_book = ttk.Button(self.button_frame, text="📚 Issue Book", command=self.issue_book_ui)
        self.button_issue_book.grid(row=1, column=1, padx=10, pady=10)

        self.button_return_book = ttk.Button(self.button_frame, text="📦 Return Book", command=self.return_book_ui)
        self.button_return_book.grid(row=2, column=0, columnspan=2, pady=20)

    def check_books_issued(self):
        if not mongo_connected:
            messagebox.showerror("Error", "Database connection not available.")
            return

        enrollment_no = self.entry_enrollment.get()
        if enrollment_no:
            results = list(book_issue_collection.find({"enrollment_no": enrollment_no}))
            if results:
                issued_books = "\n".join([f"{row['book_issued']} - Issue Date: {row['issue_date']}, Return Date: {row['return_date']}, Fine: {row['fine']}" for row in results])
                messagebox.showinfo("Books Issued", "Books issued on your name:\n" + issued_books)
            else:
                messagebox.showinfo("No Books Issued", "No books issued on your name.")
        else:
            messagebox.showerror("Error", "Please enter enrollment number.")

    def check_deadlines(self):
        if not mongo_connected:
            messagebox.showerror("Error", "Database connection not available.")
            return

        enrollment_no = self.entry_enrollment.get()
        if enrollment_no:
            results = list(book_issue_collection.find({"enrollment_no": enrollment_no}))
            if results:
                today = datetime.now().date()
                deadlines = [f"{row['book_issued']} - Deadline: {row['return_date']}" for row in results if row['return_date'] < today]
                if deadlines:
                    messagebox.showinfo("Deadlines Passed", "Deadlines passed for:\n" + "\n".join(deadlines))
                else:
                    messagebox.showinfo("No Deadlines Passed", "No deadlines passed for any books.")
            else:
                messagebox.showinfo("No Books Issued", "No books issued on your name.")
        else:
            messagebox.showerror("Error", "Please enter enrollment number.")

    def check_fine(self):
        if not mongo_connected:
            messagebox.showerror("Error", "Database connection not available.")
            return

        enrollment_no = self.entry_enrollment.get()
        if enrollment_no:
            result = book_issue_collection.aggregate([
                {"$match": {"enrollment_no": enrollment_no}},
                {"$group": {"_id": None, "total_fine": {"$sum": "$fine"}}}
            ])
            total_fine = list(result)
            if total_fine and total_fine[0]['total_fine'] > 0:
                messagebox.showinfo("Fine", f"Total fine to pay: {total_fine[0]['total_fine']}")
            else:
                messagebox.showinfo("No Fine", "No fine to pay.")
        else:
            messagebox.showerror("Error", "Please enter enrollment number.")

    def issue_book_ui(self):
        if not mongo_connected:
            messagebox.showerror("Error", "Database connection not available.")
            return

        enrollment_no = self.entry_enrollment.get()
        if enrollment_no:
            scanned_barcode = '1234567891026'
            self.issue_book(enrollment_no, scanned_barcode)
        else:
            messagebox.showerror("Error", "Please enter enrollment number.")

    def issue_book(self, enrollment_no, scanned_barcode):
        if not mongo_connected:
            messagebox.showerror("Error", "Database connection not available.")
            return

        result = student_record_collection.find_one({"enrollment_no": enrollment_no})
        if result:
            issuer_first_name, issuer_last_name, issuer_semester = result['first_name'], result['last_name'], result['semester']
            issue_date = datetime.now().date()
            return_date = issue_date + timedelta(days=7)

            book_issue_collection.insert_one({
                "book_issued": scanned_barcode,
                "issue_date": issue_date,
                "return_date": return_date,
                "enrollment_no": enrollment_no,
                "issuer_first_name": issuer_first_name,
                "issuer_last_name": issuer_last_name,
                "issuer_semester": issuer_semester,
                "status": "issued",
                "fine": 0.0
            })
            messagebox.showinfo("Success", "Book issued successfully.")
        else:
            messagebox.showerror("Error", "Student record not found.")

    def return_book_ui(self):
        if not mongo_connected:
            messagebox.showerror("Error", "Database connection not available.")
            return

        enrollment_no = self.entry_enrollment.get()
        if enrollment_no:
            scanned_barcode = '1234567891026'
            self.return_book(enrollment_no, scanned_barcode)
        else:
            messagebox.showerror("Error", "Please enter enrollment number.")

    def return_book(self, enrollment_no, scanned_barcode):
        if not mongo_connected:
            messagebox.showerror("Error", "Database connection not available.")
            return

        result = book_issue_collection.find_one({"book_issued": scanned_barcode, "enrollment_no": enrollment_no})
        if result:
            issue_date, return_date = result['issue_date'], result['return_date']
            today = datetime.now().date()
            if today > return_date:
                days_late = (today - return_date).days
                fine = days_late * 0.5
                book_issue_collection.update_one(
                    {"book_issued": scanned_barcode, "enrollment_no": enrollment_no},
                    {"$set": {"fine": fine}}
                )
                messagebox.showinfo("Success", f"Book returned with a fine of ${fine:.2f}")
            else:
                book_issue_collection.delete_one({"book_issued": scanned_barcode, "enrollment_no": enrollment_no})
                messagebox.showinfo("Success", "Book returned successfully.")
        else:
            messagebox.showerror("Error", "Book not issued to this student.")

if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
