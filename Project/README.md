#                   GROUP 1 
- BINDU KABUSARA JOSUE  S22B13/011      A98694
- MASAI ABUSOLOM        S23B13/119      B25709
- ISAAC OGUSUL          S22B13/017


# E-Library System

## Overview
The E-Library System is a simple Python program that simulates a library management system. It allows users to log in as either students or librarians, search for books, borrow and return books, and perform librarian-specific functions like adding and removing books.

## Features
- User Authentication: Students and librarians can log in with their usernames and passwords.
- Book Management: Librarians can add, remove, and view books in the library. Books can be of two types: EBooks and Print Books.
- Borrowing and Returning Books: Students can borrow and return books. The due date is automatically set to 14 days from the borrowing date.
- File Persistence: The program saves the collection of books to a CSV file (`books.csv`) and reads from it at startup.

## Classes
- Book: Represents a generic book with attributes like title, author, ISBN, etc.
- EBook and PrintBook: Subclasses of Book, representing electronic and print books, respectively.
- Person: Represents a generic person with a username and hashed password.
- User: Subclass of Person, representing a student with the ability to borrow and return books.
- Library: Manages the collection of books, user authentication, and basic book operations.
- EnhancedLibrary: Extends Library with additional features like saving and loading books from a CSV file.
- Librarian: Subclass of Person, representing a librarian with additional capabilities for book and user management.

## Usage
1. Run the program using `python filename.py`.
2. Choose between logging in as a student or librarian.
3. Follow the prompts to perform various actions, such as searching for books, borrowing, returning, adding, and removing books.

## Files
- books.csv: CSV file used for persisting the book collection.
- credentials.txt: Text file used for storing usernames and hashed passwords of users.
- Librarian.txt: Text file used for storing usernames and hashed passwords of librarians.

## Contributors
- BINDU KABUSARA JOSUE  S22B13/011      A98694
- MASAI ABUSOLOM        S23B13/119      B25709
- ISAAC OGUSUL          S22B13/017