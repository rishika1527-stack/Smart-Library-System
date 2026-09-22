-- ============================================================
-- SMART LIBRARY MANAGEMENT SYSTEM
-- Database: SQLite
-- ============================================================

-- Books Table
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    category TEXT,
    available TEXT,
    due_date TEXT
);

-- Contacts Table
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    message TEXT
);

-- Seats Table
CREATE TABLE IF NOT EXISTS seats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seat_number TEXT,
    status TEXT
);

-- ============================================================
-- SQL OPERATIONS USED IN THE APPLICATION
-- ============================================================

-- INSERT: Add a book
INSERT INTO books(title, author, category, available, due_date)
VALUES ('Example Book', 'Example Author', 'Example Category', 'Yes', NULL);

-- SELECT: View all books
SELECT * FROM books;

-- SELECT: Search books by title
SELECT * FROM books
WHERE title LIKE '%Python%';

-- UPDATE: Edit a book
UPDATE books
SET title = 'Updated Title',
    author = 'Updated Author',
    category = 'Updated Category',
    available = 'Yes'
WHERE id = 1;

-- DELETE: Delete a book
DELETE FROM books
WHERE id = 1;

-- UPDATE: Borrow a book
UPDATE books
SET available = 'Borrowed',
    due_date = 'YYYY-MM-DD'
WHERE id = 1;

-- UPDATE: Return a book
UPDATE books
SET available = 'Yes',
    due_date = NULL
WHERE id = 1;

-- COUNT: Total books
SELECT COUNT(*) FROM books;

-- COUNT: Available books
SELECT COUNT(*) FROM books
WHERE available = 'Yes';

-- COUNT: Borrowed books
SELECT COUNT(*) FROM books
WHERE available = 'Borrowed';

-- CONTACTS: View contact messages
SELECT * FROM contacts;

-- CONTACTS: Insert contact message
INSERT INTO contacts(name, email, message)
VALUES ('Student Name', 'student@example.com', 'Message');

-- SEATS: Total seats
SELECT COUNT(*) FROM seats;

-- SEATS: Occupied seats
SELECT COUNT(*) FROM seats
WHERE status = 'Occupied';

-- SEATS: Available seats
SELECT COUNT(*) FROM seats
WHERE status = 'Available';

-- SEATS: Display seats
SELECT * FROM seats
ORDER BY id;

-- BORROWED BOOKS
SELECT * FROM books
WHERE available = 'Borrowed';

-- DUE DATES
SELECT title, due_date
FROM books
WHERE available = 'Borrowed';

-- SEARCH: Title, category, or author
SELECT * FROM books
WHERE title LIKE '%keyword%'
   OR category LIKE '%keyword%'
   OR author LIKE '%keyword%';

-- ============================================================
-- END OF SQL SCRIPT
-- ============================================================