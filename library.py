from database import SessionLocal

from loan import Loan
from repositories.book_repository import BookRepository
from repositories.member_repository import MemberRepository
from repositories.loan_repository import LoanRepository


class Library:
    """
    Manages books, members, and loans.

    Business rules remain here.
    Repositories handle database operations.
    """

    def __init__(self, session=None):
        self.session = session or SessionLocal()

        self.book_repository = BookRepository(self.session)
        self.member_repository = MemberRepository(self.session)
        self.loan_repository = LoanRepository(self.session)

    # ============================================================
    # Books
    # ============================================================

    def add_book(self, book):
        """Add a book if its ID does not already exist."""

        if book.book_id is not None:
            if self.search_book(book.book_id):
                return None

        return self.book_repository.add(book)

    def delete_book(self, book):
        """Delete a book if it exists and is not borrowed."""

        stored_book = self.search_book(book.book_id)

        if stored_book is None:
            return None

        if not stored_book.is_available:
            return None

        result = self.book_repository.delete(stored_book)

        if result:
            return book

        return None

    def update_book(self, book, title, author, publish_year):
        """Update an existing book."""

        stored_book = self.search_book(book.book_id)

        if stored_book is None:
            return None

        stored_book.title = title
        stored_book.author = author
        stored_book.publish_year = publish_year

        result = self.book_repository.update(stored_book)

        if result:
            book.title = title
            book.author = author
            book.publish_year = publish_year

            return book

        return None

    def search_book(self, book_id):
        """Find a book by ID."""

        return self.book_repository.get_by_id(book_id)

    def view_all_books(self):
        """Return all books."""

        return self.book_repository.get_all()

    # ============================================================
    # Members
    # ============================================================

    def add_member(self, member):
        """Add a member if their ID does not already exist."""

        if member.member_id is not None:
            if self.search_member(member.member_id):
                return None

        return self.member_repository.add(member)

    def update_member(
        self,
        member,
        name,
        phone_number,
        email
    ):
        """Update an existing member."""

        stored_member = self.search_member(member.member_id)

        if stored_member is None:
            return None

        stored_member.name = name
        stored_member.phone_number = phone_number
        stored_member.email = email

        result = self.member_repository.update(stored_member)

        if result:
            member.name = name
            member.phone_number = phone_number
            member.email = email

            return member

        return None

    def delete_member(self, member):
        """Delete a member if they have no active loans."""

        stored_member = self.search_member(member.member_id)

        if stored_member is None:
            return None

        loans = self.loan_repository.get_by_member_id(
            member.member_id
        )

        if loans:
            return None

        result = self.member_repository.delete(stored_member)

        if result:
            return member

        return None

    def search_member(self, member_id):
        """Find a member by ID."""

        return self.member_repository.get_by_id(member_id)

    def view_all_members(self):
        """Return all members."""

        return self.member_repository.get_all()

    # ============================================================
    # Loans
    # ============================================================

    def borrow_book(self, member, book):
        """Create a loan if the member and book are valid."""

        stored_member = self.search_member(member.member_id)
        stored_book = self.search_book(book.book_id)

        if stored_member is None:
            return None

        if stored_book is None:
            return None

        if not stored_book.is_available:
            return None

        # Create domain loan using the objects supplied to Library.
        loan = Loan(member, book)

        self.loan_repository.add(loan)

        # Update database state.
        stored_book.is_available = False
        self.book_repository.update(stored_book)

        # Update the caller's domain object as well.
        book.is_available = False

        return loan

    def return_book(self, book):
        """Return a borrowed book."""

        stored_book = self.search_book(book.book_id)

        if stored_book is None:
            return None

        loan = self.loan_repository.get_by_book_id(
            book.book_id
        )

        if loan is None:
            return None

        # Update database.
        stored_book.is_available = True
        self.book_repository.update(stored_book)

        # Update domain object.
        book.is_available = True

        self.loan_repository.delete(loan)

        return Loan(
            loan.member,
            book
        )

    def view_borrowed_books(self):
        """Return all active loans."""

        return self.loan_repository.get_all()

    def close(self):
        """Close the database session."""

        self.session.close()