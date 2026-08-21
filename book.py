"""
class Book:
    def __init__(self,book_id,title,author,publish_year,is_available=True):
        self.book_id=book_id
        self.title=title
        self.author=author
        self.publish_year=publish_year
        self.is_available=is_available

    def display_book_info(self):
        print(f"book_ID: {self.book_id}\nTitle: {self.title}\nAuthor: {self.author}\nPublish Year: {self.publish_year}\nIs available: {self.is_available}")
"""


class Book:
    """
    Represents a book in the library.
    """

    def __init__(self, book_id, title, author, publish_year, is_available=True):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.publish_year = publish_year
        self.is_available = is_available

    def display_book_info(self):
        """Display the book's information."""
        print(
            f"Book ID: {self.book_id}\n"
            f"Title: {self.title}\n"
            f"Author: {self.author}\n"
            f"Publish Year: {self.publish_year}\n"
            f"Is Available: {self.is_available}"
        )

