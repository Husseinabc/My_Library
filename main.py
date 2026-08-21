import os
import time
from library import Library
from book import Book
from member import Member


library = Library()

def show_main_menu():
    print("\n========== Library Management System ==========")
    print("1. Books")
    print("2. Members")
    print("3. Loans")
    print("4. Exit")


def show_books_menu():
    print("\n========== Books Menu ==========")
    print("1. Add Book")
    print("2. Update Book")
    print("3. Delete Book")
    print("4. Search Book")
    print("5. View All Books")
    print("6. Back")


def show_members_menu():
    print("\n========== Members Menu ==========")
    print("1. Add Member")
    print("2. Update Member")
    print("3. Delete Member")
    print("4. Search Member")
    print("5. View All Members")
    print("6. Back")


def show_loans_menu():
    print("\n========== Loans Menu ==========")
    print("1. Borrow Book")
    print("2. Return Book")
    print("3. View Borrowed Books")
    print("4. Back")


while True:

    show_main_menu()

    choice = input("Choose an option: ")

    if choice == "1":

        while True:

            show_books_menu()

            book_choice = input("Choose an option: ")

            if book_choice == "1":

                book_id = int(input("Enter Book ID: "))
                title = input("Enter Book Title: ")
                author = input("Enter Author Name: ")
                publish_year = int(input("Enter Publish Year: "))

                new_book = Book(book_id, title, author, publish_year)

                if library.add_book(new_book):
                    print("Book added successfully.")
                else:
                    print("Book ID already exists.")

            elif book_choice == "2":

                book_id = int(input("Enter Book ID: "))

                book = library.search_book(book_id)

                if book:

                    title = input("Enter New Title: ")
                    author = input("Enter New Author: ")
                    publish_year = int(input("Enter New Publish Year: "))

                    library.update_book(book, title, author, publish_year)

                    print("Book updated successfully.")

                else:
                    print("Book not found.")

            elif book_choice == "3":

                book_id = int(input("Enter Book ID: "))

                book = library.search_book(book_id)

                if book:

                    if library.delete_book(book):
                        print("Book deleted successfully.")
                    else:
                        print("Cannot delete borrowed book.")

                else:
                    print("Book not found.")

            elif book_choice == "4":

                book_id = int(input("Enter Book ID: "))

                book = library.search_book(book_id)

                if book:
                    book.display_book_info()
                else:
                    print("Book not found.")

            elif book_choice == "5":

                books = library.view_all_books()

                if books:
                    for book in books:
                        print("-" * 40)
                        book.display_book_info()
                else:
                    print("No books found.")

            elif book_choice == "6":
                break

            else:
                print("Invalid choice.")

    elif choice == "2":

        while True:

            show_members_menu()

            member_choice = input("Choose an option: ")

            if member_choice == "1":

                member_id = int(input("Enter Member ID: "))
                name = input("Enter Member Name: ")
                phone_number = input("Enter Phone Number: ")
                email = input("Enter Email: ")

                new_member = Member(member_id, name, phone_number, email)

                if library.add_member(new_member):
                    print("Member added successfully.")
                else:
                    print("Member ID already exists.")

            elif member_choice == "2":

                member_id = int(input("Enter Member ID: "))

                member = library.search_member(member_id)

                if member:

                    name = input("Enter New Name: ")
                    phone_number = input("Enter New Phone Number: ")
                    email = input("Enter New Email: ")

                    library.update_member(member, name, phone_number, email)

                    print("Member updated successfully.")

                else:
                    print("Member not found.")

            elif member_choice == "3":

                member_id = int(input("Enter Member ID: "))

                member = library.search_member(member_id)

                if member:

                    if library.delete_member(member):
                        print("Member deleted successfully.")
                    else:
                        print("Cannot delete member with borrowed books.")

                else:
                    print("Member not found.")

            elif member_choice == "4":

                member_id = int(input("Enter Member ID: "))

                member = library.search_member(member_id)

                if member:
                    member.display_member_info()
                else:
                    print("Member not found.")

            elif member_choice == "5":

                members = library.view_all_members()

                if members:
                    for member in members:
                        print("-" * 40)
                        member.display_member_info()
                else:
                    print("No members found.")

            elif member_choice == "6":
                break

            else:
                print("Invalid choice.")

    elif choice == "3":

        while True:

            show_loans_menu()

            loan_choice = input("Choose an option: ")

            if loan_choice == "1":

                member_id = int(input("Enter Member ID: "))
                book_id = int(input("Enter Book ID: "))

                member = library.search_member(member_id)
                book = library.search_book(book_id)

                if member and book:

                    loan = library.borrow_book(member, book)

                    if loan:
                        print("Book borrowed successfully.")
                    else:
                        print("Borrow operation failed.")

                else:
                    print("Member or Book not found.")

            elif loan_choice == "2":

                book_id = int(input("Enter Book ID: "))

                book = library.search_book(book_id)

                if book:

                    loan = library.return_book(book)

                    if loan:
                        print("Book returned successfully.")
                    else:
                        print("This book is not currently borrowed.")

                else:
                    print("Book not found.")

            elif loan_choice == "3":

                loans = library.view_borrowed_books()

                if loans:

                    for loan in loans:
                        print("-" * 40)
                        loan.display_loan_info()

                else:
                    print("No borrowed books.")

            elif loan_choice == "4":
                break

            else:
                print("Invalid choice.")

    elif choice == "4":
        print("Thank you for using the Library Management System.")
        break

    else:
        print("Invalid choice.")