from book import Book
from member import Member
from library import Library


# ============================================================
# Fixtures / Helper Functions
# ============================================================

def create_library():
    # ننشئ Library جديدة لكل اختبار
    # حتى لا تتداخل بيانات اختبار مع اختبار آخر
    return Library()


def create_book(book_id=1):
    # دالة مساعدة لإنشاء كتاب بسرعة
    return Book(
        book_id,
        "Python Basics",
        "John Smith",
        2025
    )


def create_member(member_id=1):
    # دالة مساعدة لإنشاء عضو بسرعة
    return Member(
        member_id,
        "Ahmed",
        "0500000000",
        "ahmed@example.com"
    )


# ============================================================
# Book Tests
# ============================================================

def test_add_book():
    library = create_library()
    book = create_book()

    # نضيف الكتاب إلى المكتبة
    result = library.add_book(book)

    # يجب أن تعيد العملية الكتاب عند نجاحها
    assert result is book

    # يجب أن يصبح الكتاب موجودًا داخل قائمة الكتب
    assert book in library.books


def test_cannot_add_book_with_duplicate_id():
    library = create_library()

    first_book = create_book(1)
    second_book = create_book(1)

    # إضافة الكتاب الأول يجب أن تنجح
    assert library.add_book(first_book) is first_book

    # إضافة كتاب بنفس الـ ID يجب أن تفشل
    assert library.add_book(second_book) is None

    # يجب أن يبقى لدينا كتاب واحد فقط
    assert len(library.books) == 1


def test_search_book():
    library = create_library()
    book = create_book()

    library.add_book(book)

    # البحث باستخدام الـ ID
    result = library.search_book(1)

    # يجب أن نجد نفس الكتاب
    assert result is book


def test_search_nonexistent_book():
    library = create_library()

    # البحث عن كتاب غير موجود
    result = library.search_book(999)

    # يجب أن تكون النتيجة None
    assert result is None


def test_update_book():
    library = create_library()
    book = create_book()

    library.add_book(book)

    # تحديث بيانات الكتاب
    result = library.update_book(
        book,
        "Advanced Python",
        "Jane Smith",
        2026
    )

    # العملية يجب أن تعيد نفس الكتاب
    assert result is book

    # نتأكد أن البيانات تغيرت
    assert book.title == "Advanced Python"
    assert book.author == "Jane Smith"
    assert book.publish_year == 2026


def test_delete_book():
    library = create_library()
    book = create_book()

    library.add_book(book)

    # حذف الكتاب
    result = library.delete_book(book)

    # يجب أن تعيد العملية الكتاب
    assert result is book

    # يجب ألا يبقى الكتاب في المكتبة
    assert book not in library.books


def test_cannot_delete_borrowed_book():
    library = create_library()

    book = create_book()
    member = create_member()

    library.add_book(book)
    library.add_member(member)

    # نستعير الكتاب أولًا
    loan = library.borrow_book(member, book)

    assert loan is not None
    assert book.is_available is False

    # محاولة حذف كتاب مستعار يجب أن تفشل
    result = library.delete_book(book)

    assert result is None

    # الكتاب يجب أن يبقى موجودًا
    assert book in library.books


# ============================================================
# Member Tests
# ============================================================

def test_add_member():
    library = create_library()
    member = create_member()

    # إضافة العضو
    result = library.add_member(member)

    assert result is member
    assert member in library.members


def test_cannot_add_member_with_duplicate_id():
    library = create_library()

    first_member = create_member(1)
    second_member = create_member(1)

    # إضافة العضو الأول
    assert library.add_member(first_member) is first_member

    # العضو الثاني لديه نفس الـ ID
    assert library.add_member(second_member) is None

    # يجب أن يبقى عضو واحد فقط
    assert len(library.members) == 1


def test_search_member():
    library = create_library()
    member = create_member()

    library.add_member(member)

    result = library.search_member(1)

    assert result is member


def test_search_nonexistent_member():
    library = create_library()

    result = library.search_member(999)

    assert result is None


def test_update_member():
    library = create_library()
    member = create_member()

    library.add_member(member)

    # تحديث بيانات العضو
    result = library.update_member(
        member,
        "Mohammed",
        "0555555555",
        "mohammed@example.com"
    )

    assert result is member

    # التأكد من تحديث البيانات
    assert member.name == "Mohammed"
    assert member.phone_number == "0555555555"
    assert member.email == "mohammed@example.com"


def test_delete_member():
    library = create_library()
    member = create_member()

    library.add_member(member)

    result = library.delete_member(member)

    assert result is member
    assert member not in library.members


def test_cannot_delete_member_with_loan():
    library = create_library()

    member = create_member()
    book = create_book()

    library.add_member(member)
    library.add_book(book)

    # العضو يستعير كتابًا
    loan = library.borrow_book(member, book)

    assert loan is not None

    # لا يجب السماح بحذف العضو أثناء وجود إعارة
    result = library.delete_member(member)

    assert result is None
    assert member in library.members


# ============================================================
# Loan Tests
# ============================================================

def test_borrow_book():
    library = create_library()

    member = create_member()
    book = create_book()

    library.add_member(member)
    library.add_book(book)

    # استعارة الكتاب
    loan = library.borrow_book(member, book)

    # يجب إنشاء Loan
    assert loan is not None

    # يجب أن يحتوي الـ Loan على العضو والكتاب الصحيحين
    assert loan.member is member
    assert loan.book is book

    # الكتاب يجب أن يصبح غير متاح
    assert book.is_available is False

    # يجب أن تضاف الإعارة إلى قائمة loans
    assert loan in library.loans


def test_cannot_borrow_unavailable_book():
    library = create_library()

    member1 = create_member(1)
    member2 = create_member(2)
    book = create_book()

    library.add_member(member1)
    library.add_member(member2)
    library.add_book(book)

    # العضو الأول يستعير الكتاب
    first_loan = library.borrow_book(member1, book)

    assert first_loan is not None

    # العضو الثاني يحاول استعارة نفس الكتاب
    second_loan = library.borrow_book(member2, book)

    # يجب أن تفشل العملية
    assert second_loan is None

    # يجب أن تبقى إعارة واحدة فقط
    assert len(library.loans) == 1


def test_cannot_borrow_book_if_member_is_not_in_library():
    library = create_library()

    member = create_member()
    book = create_book()

    # نضيف الكتاب فقط، ولا نضيف العضو
    library.add_book(book)

    # محاولة الاستعارة يجب أن تفشل
    result = library.borrow_book(member, book)

    assert result is None

    # الكتاب يجب أن يبقى متاحًا
    assert book.is_available is True


def test_cannot_borrow_book_if_book_is_not_in_library():
    library = create_library()

    member = create_member()
    book = create_book()

    # نضيف العضو فقط
    library.add_member(member)

    # الكتاب غير موجود في المكتبة
    result = library.borrow_book(member, book)

    assert result is None


def test_return_book():
    library = create_library()

    member = create_member()
    book = create_book()

    library.add_member(member)
    library.add_book(book)

    # استعارة الكتاب
    loan = library.borrow_book(member, book)

    assert loan is not None
    assert book.is_available is False

    # إرجاع الكتاب
    returned_loan = library.return_book(book)

    # يجب إرجاع نفس الـ Loan
    assert returned_loan is loan

    # الكتاب يجب أن يصبح متاحًا مرة أخرى
    assert book.is_available is True

    # يجب حذف الـ Loan من قائمة الإعارات
    assert loan not in library.loans


def test_return_book_that_is_not_borrowed():
    library = create_library()
    book = create_book()

    library.add_book(book)

    # محاولة إرجاع كتاب غير مستعار
    result = library.return_book(book)

    assert result is None