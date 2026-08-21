from book import Book as DomainBook
from member import Member as DomainMember
from loan import Loan as DomainLoan

from database import SessionLocal

from repositories.book_repository import BookRepository
from repositories.member_repository import MemberRepository
from repositories.loan_repository import LoanRepository


def test_book_repository():
    session = SessionLocal()

    try:
        repository = BookRepository(session)

        book = DomainBook(
            book_id=None,
            title="Repository Test Book",
            author="Test Author",
            publish_year=2026,
            is_available=True
        )

        repository.add(book)

        assert book.book_id is not None

        found_book = repository.get_by_id(book.book_id)

        assert found_book is not None
        assert found_book.book_id == book.book_id
        assert found_book.title == "Repository Test Book"

        book.title = "Updated Repository Test Book"

        repository.update(book)

        updated_book = repository.get_by_id(book.book_id)

        assert updated_book is not None
        assert updated_book.title == "Updated Repository Test Book"

    finally:
        if book.book_id is not None:
            repository.delete(book)

        session.close()


def test_member_repository():
    session = SessionLocal()

    try:
        repository = MemberRepository(session)

        member = DomainMember(
            member_id=None,
            name="Repository Test Member",
            phone_number="0500000000",
            email="repository@test.com"
        )

        repository.add(member)

        assert member.member_id is not None

        found_member = repository.get_by_id(member.member_id)

        assert found_member is not None
        assert found_member.name == "Repository Test Member"

        member.name = "Updated Repository Test Member"

        repository.update(member)

        updated_member = repository.get_by_id(member.member_id)

        assert updated_member is not None
        assert updated_member.name == "Updated Repository Test Member"

    finally:
        if member.member_id is not None:
            repository.delete(member)

        session.close()


def test_loan_repository():
    session = SessionLocal()

    try:
        book_repository = BookRepository(session)
        member_repository = MemberRepository(session)
        loan_repository = LoanRepository(session)

        book = DomainBook(
            book_id=None,
            title="Loan Test Book",
            author="Test Author",
            publish_year=2026,
            is_available=False
        )

        member = DomainMember(
            member_id=None,
            name="Loan Test Member",
            phone_number="0511111111",
            email="loan@test.com"
        )

        book_repository.add(book)
        member_repository.add(member)

        loan = DomainLoan(member, book)

        loan_repository.add(loan)

        found_loan = loan_repository.get_by_book_id(
            book.book_id
        )

        assert found_loan is not None
        assert found_loan.book.book_id == book.book_id
        assert found_loan.member.member_id == member.member_id

        member_loans = loan_repository.get_by_member_id(
            member.member_id
        )

        assert len(member_loans) == 1

        loan_repository.delete(loan)

    finally:
        if member.member_id is not None:
            member_repository.delete(member)

        if book.book_id is not None:
            book_repository.delete(book)

        session.close()