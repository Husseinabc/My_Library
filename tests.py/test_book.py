from book import Book


def test_book_is_created_correctly():
    # ننشئ كتابًا مثلما نفعل في البرنامج الأساسي
    book = Book(1, "Python Basics", "John Smith", 2025)

    # نتأكد أن البيانات تم حفظها بشكل صحيح
    assert book.book_id == 1
    assert book.title == "Python Basics"
    assert book.author == "John Smith"
    assert book.publish_year == 2025


def test_book_is_available_when_created():
    # القيمة الافتراضية لـ is_available يجب أن تكون True
    book = Book(1, "Python Basics", "John Smith", 2025)

    assert book.is_available is True