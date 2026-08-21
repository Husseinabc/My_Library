from sqlalchemy import select
from sqlalchemy.orm import Session

from book import Book as DomainBook
from models import Book as BookModel


class BookRepository:
    """
    Handles database operations for books.

    Converts between the Domain Book and the SQLAlchemy Book model.
    """

    def __init__(self, session: Session):
        self.session = session

    def add(self, book: DomainBook) -> DomainBook:
        """Save a domain Book in PostgreSQL."""

        db_book = BookModel(
            title=book.title,
            author=book.author,
            publish_year=book.publish_year,
            is_available=book.is_available,
        )

        self.session.add(db_book)
        self.session.commit()
        self.session.refresh(db_book)

        # Database ID becomes the domain book_id.
        book.book_id = db_book.id

        return book

    def get_by_id(self, book_id: int) -> DomainBook | None:
        """Get a book from PostgreSQL by ID."""

        statement = select(BookModel).where(BookModel.id == book_id)
        db_book = self.session.scalar(statement)

        if db_book is None:
            return None

        return self._to_domain(db_book)

    def get_all(self) -> list[DomainBook]:
        """Return all books from PostgreSQL."""

        statement = select(BookModel)
        db_books = self.session.scalars(statement).all()

        return [self._to_domain(book) for book in db_books]

    def update(self, book: DomainBook) -> DomainBook | None:
        """Update an existing book."""

        statement = select(BookModel).where(BookModel.id == book.book_id)
        db_book = self.session.scalar(statement)

        if db_book is None:
            return None

        db_book.title = book.title
        db_book.author = book.author
        db_book.publish_year = book.publish_year
        db_book.is_available = book.is_available

        self.session.commit()
        self.session.refresh(db_book)

        return book

    def delete(self, book: DomainBook) -> DomainBook | None:
        """Delete a book from PostgreSQL."""

        statement = select(BookModel).where(BookModel.id == book.book_id)
        db_book = self.session.scalar(statement)

        if db_book is None:
            return None

        self.session.delete(db_book)
        self.session.commit()

        return book

    @staticmethod
    def _to_domain(db_book: BookModel) -> DomainBook:
        """Convert SQLAlchemy model into a domain Book."""

        return DomainBook(
            book_id=db_book.id,
            title=db_book.title,
            author=db_book.author,
            publish_year=db_book.publish_year,
            is_available=db_book.is_available,
        )