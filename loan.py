"""
class Loan:
    def __init__(self,member,book):
        self.member=member
        self.book=book
        #النسخة الأولى فقط. لاحقًا يمكن إضافة:
        #•	borrow_date 
        #•	return_date 
        #•	due_date 



    def display_loan_info(self):
        self.book.display_book_info()       
        self.member.display_member_info()

"""

class Loan:
    """
    Represents a loan between a member and a book.
    """

    def __init__(self, member, book):
        self.member = member
        self.book = book

        # Future versions may include:
        # borrow_date
        # return_date
        # due_date

    def display_loan_info(self):
        """Display information about the borrowed book and member."""
        self.book.display_book_info()
        self.member.display_member_info()