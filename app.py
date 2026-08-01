from flask import Flask, render_template, request, redirect, session
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)

def init_db():
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS books(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            category TEXT,
            available TEXT,
            due_date TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS contacts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS seats(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            seat_number TEXT,
            status TEXT
        )
        """
    )

    connection.commit()
    connection.close()

init_db()
app.secret_key = "rishika_secret_key"

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        # Student login
        if email == "student@gmail.com" and password == "1234":
            session["user"] = "student"
            return redirect("/student")

        # Admin login
        elif email == "admin@gmail.com" and password == "admin123":
            session["user"] = "admin"
            return redirect("/admin")

        else:
            return "Invalid Email or Password"

    return render_template("login.html")

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# Student Dashboard
@app.route("/student")
def student():

    if session.get("user") != "student":
        return redirect("/login")

    return render_template("student_dashboard.html")

# Admin Dashboard
@app.route("/admin")
def admin():

    if session.get("user") != "admin":
        return redirect("/login")

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM books WHERE available='Yes'")
    available_books = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM books WHERE available='Borrowed'")
    borrowed_books = cursor.fetchone()[0]

    connection.close()

    return render_template(
        "admin_dashboard.html",
        total_books=total_books,
        available_books=available_books,
        borrowed_books=borrowed_books
    )

# Add Book
@app.route("/add_book", methods=["GET", "POST"])
def add_book():

    if request.method == "POST":

        title = request.form["title"]
        author = request.form["author"]
        category = request.form["category"]
        available = request.form["available"]
        due_date = request.form["due_date"]

        connection = sqlite3.connect("library.db")
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO books(title, author, category, available, due_date)
            VALUES (?, ?, ?, ?, ?)
            """,
            (title, author, category, available, due_date)
        )

        connection.commit()
        connection.close()

        return redirect("/view_books")

    return render_template("add_book.html")

# View Books
@app.route("/view_books")
def view_books():

    search = request.args.get("search", "")

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    if search:
        cursor.execute(
            "SELECT * FROM books WHERE title LIKE ?",
            ('%' + search + '%',)
        )
    else:
        cursor.execute("SELECT * FROM books")

    books = cursor.fetchall()

    connection.close()

    return render_template(
        "view_books.html",
        books=books,
        search=search
    )

# Edit Book
@app.route("/edit_book/<int:book_id>", methods=["GET", "POST"])
def edit_book(book_id):

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    if request.method == "POST":

        title = request.form["title"]
        author = request.form["author"]
        category = request.form["category"]
        available = request.form["available"]

        cursor.execute(
            """
            UPDATE books
            SET title=?, author=?, category=?, available=?
            WHERE id=?
            """,
            (title, author, category, available, book_id)
        )

        connection.commit()
        connection.close()

        return redirect("/view_books")

    cursor.execute("SELECT * FROM books WHERE id=?", (book_id,))
    book = cursor.fetchone()

    connection.close()

    return render_template("edit_book.html", book=book)

# Delete Book
@app.route("/delete_book/<int:book_id>")
def delete_book(book_id):

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM books WHERE id=?", (book_id,))

    connection.commit()
    connection.close()

    return redirect("/view_books")

# Borrow Book with Real Due Date
@app.route("/borrow_book/<int:book_id>")
def borrow_book(book_id):

    due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE books SET available='Borrowed', due_date=? WHERE id=?",
        (due_date, book_id)
    )

    connection.commit()
    connection.close()

    return redirect("/view_books")

# Return Book
@app.route("/return_book/<int:book_id>")
def return_book(book_id):

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE books SET available='Yes', due_date=NULL WHERE id=?",
        (book_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/view_books")

# AI Recommendation
@app.route("/recommend", methods=["GET", "POST"])
def recommend():

    books = []

    if request.method == "POST":

        interest = request.form["interest"]

        connection = sqlite3.connect("library.db")
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT * FROM books
            WHERE title LIKE ?
               OR category LIKE ?
               OR author LIKE ?
            """,
            ('%' + interest + '%',
             '%' + interest + '%',
             '%' + interest + '%')
        )

        books = cursor.fetchall()

        connection.close()

    return render_template("recommend.html", books=books)

# About Page
@app.route("/about")
def about():
    return render_template("about.html")

# Contact Page
@app.route("/contact", methods=["GET", "POST"])
def contact():

    success = False

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        connection = sqlite3.connect("library.db")
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO contacts(name, email, message) VALUES (?, ?, ?)",
            (name, email, message)
        )

        connection.commit()
        connection.close()

        success = True

    return render_template("contact.html", success=success)

# View Contact Messages
@app.route("/view_contacts")
def view_contacts():

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()

    connection.close()

    return render_template("view_contacts.html", contacts=contacts)

# Seats Page
@app.route("/seats")
def seats():

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM seats")
    total_seats = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM seats WHERE status='Occupied'"
    )
    occupied_seats = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM seats WHERE status='Available'"
    )
    available_seats = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM seats ORDER BY id")
    seats_data = cursor.fetchall()

    connection.close()

    return render_template(
        "seats.html",
        total_seats=total_seats,
        occupied_seats=occupied_seats,
        available_seats=available_seats,
        seats_data=seats_data
    )


# Due Dates Page
@app.route("/due_dates")
def due_dates():

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT title, due_date FROM books WHERE available='Borrowed'"
    )

    rows = cursor.fetchall()
    connection.close()

    due_books = []

    today = datetime.now().date()

    for row in rows:

        title = row[0]
        due_date_str = row[1]

        status = "On Time"
        fine = 0

        if due_date_str:

            due_date = datetime.strptime(
                due_date_str,
                "%Y-%m-%d"
            ).date()

            overdue_days = (today - due_date).days

            if overdue_days > 0:
                status = "Overdue"
                fine = overdue_days * 2

        due_books.append({
            "title": title,
            "due_date": due_date_str,
            "status": status,
            "fine": fine
        })

    return render_template(
        "due_dates.html",
        due_books=due_books
    )


# Borrowed Books Page
@app.route("/borrowed_books")
def borrowed_books():

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM books WHERE available='Borrowed'")
    books = cursor.fetchall()

    connection.close()

    return render_template("borrowed_books.html", books=books)

# Run Flask App
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
