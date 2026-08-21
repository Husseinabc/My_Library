from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


# ============================================================
# Book
# ============================================================

class Book(Base):
    """
    Database model representing a book.
    """

    __tablename__ = "books"

    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(200), nullable=False)

    author: Mapped[str] = mapped_column(String(200), nullable=False)

    publish_year: Mapped[int] = mapped_column(nullable=False)

    is_available: Mapped[bool] = mapped_column(
        default=True,
        nullable=False
    )

    # Relationship with loans
    loans: Mapped[list["Loan"]] = relationship(
        back_populates="book"
    )


# ============================================================
# Member
# ============================================================

class Member(Base):
    """
    Database model representing a library member.
    """

    __tablename__ = "members"

    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    phone_number: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    # Relationship with loans
    loans: Mapped[list["Loan"]] = relationship(
        back_populates="member"
    )


# ============================================================
# Loan
# ============================================================

class Loan(Base):
    """
    Database model representing a book loan.
    """

    __tablename__ = "loans"

    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True)

    # Foreign Keys
    member_id: Mapped[int] = mapped_column(
        ForeignKey("members.id"),
        nullable=False
    )

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id"),
        nullable=False
    )

    # Relationships
    member: Mapped["Member"] = relationship(
        back_populates="loans"
    )

    book: Mapped["Book"] = relationship(
        back_populates="loans"
    )

# ============================================================
# User
# ============================================================

class User(Base):
    """
    Database model representing an authenticated user.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        nullable=False
    )

    hashed_password: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    google_id: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        nullable=True
    )