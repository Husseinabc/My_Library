from sqlalchemy import select
from sqlalchemy.orm import Session

from book import Book as DomainBook
from loan import Loan as DomainLoan
from member import Member as DomainMember
from models import Loan as LoanModel


class LoanRepository:
    """
    Handles database operations for loans.

    Converts between Domain Loan objects and SQLAlchemy Loan models.
    """

    def __init__(self, session: Session):
        self.session = session

    def add(self, loan: DomainLoan) -> DomainLoan:
        """Save a loan in PostgreSQL."""

        db_loan = LoanModel(
            member_id=loan.member.member_id,
            book_id=loan.book.book_id,
        )

        self.session.add(db_loan)
        self.session.commit()
        self.session.refresh(db_loan)

        return loan

    def get_by_id(self, loan_id: int) -> DomainLoan | None:
        """Get a loan by its ID."""

        statement = select(LoanModel).where(LoanModel.id == loan_id)
        db_loan = self.session.scalar(statement)

        if db_loan is None:
            return None

        return self._to_domain(db_loan)

    def get_all(self) -> list[DomainLoan]:
        """Return all loans."""

        statement = select(LoanModel)
        db_loans = self.session.scalars(statement).all()

        return [self._to_domain(loan) for loan in db_loans]

    def get_by_book_id(self, book_id: int) -> DomainLoan | None:
        """Find the loan associated with a book."""

        statement = select(LoanModel).where(
            LoanModel.book_id == book_id
        )

        db_loan = self.session.scalar(statement)

        if db_loan is None:
            return None

        return self._to_domain(db_loan)

    def get_by_member_id(
        self,
        member_id: int
    ) -> list[DomainLoan]:
        """Return all loans belonging to a member."""

        statement = select(LoanModel).where(
            LoanModel.member_id == member_id
        )

        db_loans = self.session.scalars(statement).all()

        return [self._to_domain(loan) for loan in db_loans]

    def delete(self, loan: DomainLoan) -> DomainLoan | None:
        """Delete a loan from PostgreSQL."""

        statement = select(LoanModel).where(
            LoanModel.member_id == loan.member.member_id,
            LoanModel.book_id == loan.book.book_id,
        )

        db_loan = self.session.scalar(statement)

        if db_loan is None:
            return None

        self.session.delete(db_loan)
        self.session.commit()

        return loan

    def _to_domain(self, db_loan: LoanModel) -> DomainLoan:
        """Convert SQLAlchemy Loan model into a Domain Loan."""

        member = DomainMember(
            member_id=db_loan.member.id,
            name=db_loan.member.name,
            phone_number=db_loan.member.phone_number,
            email=db_loan.member.email,
        )

        book = DomainBook(
            book_id=db_loan.book.id,
            title=db_loan.book.title,
            author=db_loan.book.author,
            publish_year=db_loan.book.publish_year,
            is_available=db_loan.book.is_available,
        )

        return DomainLoan(member, book)