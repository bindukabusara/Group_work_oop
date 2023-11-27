import hashlib
import getpass
import csv
from datetime import datetime, timedelta

class Book:
    def __init__(self, title, author, ISBN):
        self.title = title
        self.author = author
        self.ISBN = ISBN
        self.borrowed = False
        self.borrower = None
        self.due_date = None

    def is_overdue(self):
        if self.borrowed and self.due_date < datetime.now():
            return True
        return False

    def __str__(self):
        return f"{self.title} by {self.author}"
    
class EBook(Book):
    def __init__(self, title, author, ISBN, file_format):
        super().__init__(title, author, ISBN)
        self.file_format = file_format  # e.g., PDF, EPUB

    def __str__(self):
        return f"[EBook - {self.file_format}] {self.title} by {self.author}"

class PrintBook(Book):
    def __init__(self, title, author, ISBN, pages):
        super().__init__(title, author, ISBN)
        self.pages = pages  # number of pages

    def __str__(self):
        return f"[Print Book - {self.pages} pages] {self.title} by {self.author}"

class Person:
    def __init__(self, username, password):
        self.username = username
        self.password = self._hash_password(password)
    
    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password):
        return self.password == self._hash_password(password)

    def __str__(self):
        return self.username
class User(Person):
    def __init__(self, username, user_type, password):
        super().__init__(username, password)
        self.user_type = user_type
        self.borrowed_books = []

    def borrow_book(self, book):
        if not book.borrowed:
            book.borrowed = True
            book.borrower = self
            book.due_date = datetime.now() + timedelta(days=14)
            self.borrowed_books.append(book)
            return f"{self.username} has borrowed {book.title}."
        else:
            return f"{book.title} is already borrowed ."

    def return_book(self, book):
        # Debug print statements
        print(f"Attempting to return: {book.title}")
        print(f"Books currently borrowed by {self.username}: {[b.title for b in self.borrowed_books]}")

        if book in self.borrowed_books:
            book.borrowed = False
            book.borrower = None
            book.due_date = None
            self.borrowed_books.remove(book)
            return f"{self.username} has returned {book.title}."
        else:
            return f"{self.username} didn't borrow {book.title}."

    def __str__(self):
        return self.name

class Library:
    def __init__(self):
        self.collection = []
        self.users = []
        self.usernames = {}

    def add_book(self, book):
        self.collection.append(book)

    def remove_book(self, book):
        if book in self.collection:
            self.collection.remove(book)

    def search_books(self, query, search_type="title"):
        if search_type == "title":
            return [book for book in self.collection if query.lower() in book.title.lower()]
        elif search_type == "author":
            return [book for book in self.collection if query.lower() in book.author.lower()]
    def get_user(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None
    def due_soon_notifications(self):
        notifications = []
        for book in self.collection:
            if book.borrowed and (book.due_date - datetime.now()).days <= 3:
                notifications.append(f"{book.borrower.name}, your book '{book.title}' is due on {book.due_date.date()}. Please return it on time.")
        return notifications

    def authenticate_user(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            with open("credentials.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    stored_username, stored_hashed_password = line.strip().split(',')
                    if stored_username == username and stored_hashed_password == hashed_password:
                        return True
        except FileNotFoundError:
            pass

        return False   
    
    def register_user(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        # Check if user already exists
        try:
            with open("credentials.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    stored_username, _ = line.strip().split(',')
                    if stored_username == username:
                        return "User already exists!"
        except FileNotFoundError:
            pass

        # If user does not exist, store the new credentials
        with open("credentials.txt", "a") as file:
            file.write(f"{username},{hashed_password}\n")
        return "User registered successfully!"

    def __str__(self):
        return f"Library has {len(self.collection)} books."

    def get_user(self, username):
        # Fetch the user object based on the username
        for user in self.users:
            if user.username == username:
                return user
        return None

    def borrow_book(self, user, book_title):
        # Search for the book in the library's collection
        for book in self.collection:
            if book.title == book_title:
                return user.borrow_book(book)
        return f"Book titled '{book_title}' not found in the library."

    def return_book(self, user, book_title):
        # Search for the book in the library's collection
        for book in self.collection:
            if book.title == book_title:
                return user.return_book(book)
        return f"Book titled '{book_title}' not found in the library."
    
class EnhancedLibrary(Library):

    def save_books_to_file(self):
        with open("books.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["title", "author", "ISBN", "type", "status", "borrower", "due_date"])
            for book in self.collection:
                if isinstance(book, EBook):
                    book_type = "EBook"
                elif isinstance(book, PrintBook):
                    book_type = "PrintBook"
                else:
                    book_type = "Unknown"
                
                status = "borrowed" if book.borrowed else "available"
                borrower = book.borrower.username if book.borrower else ""
                due_date = book.due_date.strftime('%Y-%m-%d') if book.due_date else ""
                
                writer.writerow([book.title, book.author, book.ISBN, book_type, status, borrower, due_date])

    def load_books_from_file(self):
        self.collection = []  # clear current collection
        try:
            with open("books.csv", "r") as file:
                reader = csv.reader(file)
                next(reader)  # skip header row
                
                for row in reader:
                    title, author, ISBN, book_type, status, borrower, due_date = row
                    if book_type == "EBook":
                        book = EBook(title, author, ISBN, "")
                    elif book_type == "PrintBook":
                        book = PrintBook(title, author, ISBN, 0)  # placeholder values for format and pages
                    else:
                        book = Book(title, author, ISBN)
                    
                    book.borrowed = True if status == "borrowed" else False
                    book.borrower = self.get_user(borrower) if borrower else None
                    book.due_date = datetime.strptime(due_date, '%Y-%m-%d') if due_date else None
                    
                    self.collection.append(book)
        except FileNotFoundError:
            pass

    def add_new_ebook(self, title, author, ISBN, file_format):
        ebook = EBook(title, author, ISBN, file_format)
        self.add_book(ebook)

    def add_new_printbook(self, title, author, ISBN, pages):
        printbook = PrintBook(title, author, ISBN, pages)
        self.add_book(printbook)
        
    def authenticate_librarian(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            with open("Librarian.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    stored_username, stored_hashed_password = line.strip().split(',')
                    if stored_username == username and stored_hashed_password == hashed_password:
                        return True
        except FileNotFoundError:
            pass

        return False

    def borrow_book(self, user, book_title):
        # Read the CSV
        with open("books.csv", "r") as file:
            rows = list(csv.reader(file))
            for idx, row in enumerate(rows):
                title = row[0]
                if title == book_title:
                    if row[4] == "available":  # Check status column
                        row[4] = "borrowed"
                        row[5] = user.username
                        row[6] = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
                        break
                    else:
                        return f"{book_title} is already borrowed."
            else:
                return f"Book titled '{book_title}' not found in the library."

        # Update the CSV
        with open("books.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        return f"{user.username} has borrowed {book_title}."

    
    def return_book(self, user, book_title):
        # Read the CSV
        with open("books.csv", "r") as file:
            rows = list(csv.reader(file))
            for idx, row in enumerate(rows):
                title = row[0]
                if title == book_title:
                    if row[4] == "borrowed" and row[5] == user.username:  # Check status and borrower columns
                        row[4] = "available"
                        row[5] = ""
                        row[6] = ""
                        break
                    else:
                        return f"{book_title} is not borrowed by {user.username}."
            else:
                return f"Book titled '{book_title}' not found in the library."

        # Update the CSV
        with open("books.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        return f"{user.username} has returned {book_title}."

class Librarian(Person):
    def __init__(self, username, password):
        super().__init__(username, password)

    def add_new_ebook(self, library, title, author, ISBN, file_format):
        ebook = EBook(title, author, ISBN, file_format)
        library.add_book(ebook)

    def add_new_printbook(self, library, title, author, ISBN, pages):
        printbook = PrintBook(title, author, ISBN, pages)
        library.add_book(printbook)

    def remove_book_by_title(self, library, title):
        for book in library.collection:
            if book.title == title:
                library.remove_book(book)
                return f"Book titled '{title}' removed successfully!"
        return f"Book titled '{title}' not found in the library."
    
    @staticmethod
    def register_librarian():
        username = input("Enter librarian username: ")
        password = input("Enter librarian password: ")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Check if librarian already exists
        try:
            with open("Librarian.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    stored_username, _ = line.strip().split(',')
                    if stored_username == username:
                        print("Librarian already exists!")
                        return
        except FileNotFoundError:
            pass

        # If librarian does not exist, store the new credentials
        with open("Librarian.txt", "a") as file:
            file.write(f"{username},{hashed_password}\n")
        print("Librarian registered successfully!")
  
def librarian_menu(librarian, library):
    print(f"Welcome back {librarian.username} (Librarian)")
    print("1. Add New Book\n2. Remove Book\n3. View All Books\n4. Save Collection to CSV\n5. Register a new Librarian\n6. Exit\n")
    choice = int(input("Enter your choice: "))
    while choice != 6:
        if choice == 1:
            add_new_book_as_librarian(librarian, library)
        elif choice == 2:
            remove_book_as_librarian(librarian, library)
        elif choice == 3:
            view_all_books(library)
        elif choice == 4:
            library.save_books_to_file()
            print("Books collection saved to CSV!")
        elif choice == 5:
            Librarian.register_librarian()
        print("1. Add New Book\n2. Remove Book\n3. View All Books\n4. Save Collection to CSV\n5. Register a new Librarian\n6. Exit\n")
        choice = int(input("Enter your choice: "))

def add_new_book_as_librarian(librarian, library):
    book_type = input("Enter book type (EBook/PrintBook): ").strip().lower()
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    ISBN = input("Enter book ISBN: ")
    
    if book_type == "ebook":
        file_format = input("Enter eBook file format (e.g., PDF, EPUB): ")
        librarian.add_new_ebook(library, title, author, ISBN, file_format)
        print(f"EBook titled '{title}' added successfully!")
    elif book_type == "printbook":
        pages = int(input("Enter number of pages: "))
        librarian.add_new_printbook(library, title, author, ISBN, pages)
        print(f"Print Book titled '{title}' added successfully!")
    else:
        print("Invalid book type!")

def remove_book_as_librarian(librarian, library):
    book_title = input("Enter book title to remove: ")
    print(librarian.remove_book_by_title(library, book_title))

def view_all_books(library):
    if library.collection:
        for book in library.collection:
            print(book)
    else:
        print("No books available in the library.")


def main():
    # Creating a library instance
    lib = EnhancedLibrary()
    lib.load_books_from_file()  # Load books from file at the start

    def welcome():
        print("welcome to the E-Library System\n")
        print("1. Login\n2. Register\n3. Exit\n")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            role = input("Enter role (student/librarian): ").strip().lower()
            username = input("Enter username: ")
            password = getpass.getpass("Enter your password: ")

            if role == "student":
                if lib.authenticate_user(username, password):
                    user = lib.get_user(username)
                    if not user:
                        user = User(username, 'student', password)
                        lib.users.append(user)
                    menu(user, username)
                else:
                    print("Student not found or incorrect password!")

            elif role == "librarian":
                if lib.authenticate_librarian(username, password):
                    librarian = Librarian(username, password)
                    librarian_menu(librarian, lib)
                else:
                    print("Librarian not found or incorrect password!")
            else:
                print("Invalid role!")
                welcome()
        elif choice == 2:
            username = input("Enter username: ")
            password = getpass.getpass("Enter your password: ")
            if lib.register_user(username, password) == "User registered successfully!":
                user = User(username, 'student', password)
                lib.users.append(user)
                menu(user, username)
            else:
                print(lib.register_user(username, password))
        elif choice == 3:
            lib.save_books_to_file()  # Save books to file before exiting
            print("Goodbye!")
            exit()

    def menu(user,username):
        print(f"Welcome back {username}")
        print("1. Search Books\n2. Borrow Book\n3. Return Book\n4. Exit\n")
        choice = int(input("Enter your choice: "))
        while choice != 4:
            if choice == 1:
                search_books()
            elif choice == 2:
                borrow_book(user)
            elif choice == 3:
                return_book(user)
            print("1. Search Books\n2. Borrow Book\n3. Return Book\n4. Exit\n")
            choice = int(input("Enter your choice: "))

    def search_books():
        search_type = input("Enter search type (title/author): ")
        query = input("Enter search query: ")
        results = lib.search_books(query, search_type)
        if results:
            for book in results:
                print(book)  # This will use the __str__ method of the Book class
        else:
            print("No books found matching the query.")
    
    def borrow_book(user):
        book_title = input("Enter book title: ")
        print(lib.borrow_book(user, book_title))

    def return_book(user):
        book_title = input("Enter book title: ")
        print(lib.return_book(user, book_title))

    welcome()
if __name__ == "__main__":
    main()