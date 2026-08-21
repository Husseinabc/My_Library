from book import Book
from member import Member
from loan import Loan


def test_loan_connects_member_and_book():
    # ننشئ كتابًا وعضوًا
    book = Book(1, "Python Basics", "John Smith", 2025)
    member = Member(
        1,
        "Ahmed",
        "0500000000",
        "ahmed@example.com"
    )

    # ننشئ عملية إعارة
    loan = Loan(member, book)

    # نتأكد أن الـ Loan مرتبط بالعضو والكتاب الصحيحين
    assert loan.member is member
    assert loan.book is book