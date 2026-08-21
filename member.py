"""
class Member:
    def __init__(self,member_id,name,phone_number,email):
        self.member_id=member_id
        self.name=name
        self.phone_number=phone_number
        self.email=email

    def display_member_info(self):
        print(f"member id: {self.member_id}\nname: {self.name}\nphone number: {self.phone_number}\nemail: {self.email}")

"""

class Member:
    """
    Represents a library member.
    """

    def __init__(self, member_id, name, phone_number, email):
        self.member_id = member_id
        self.name = name
        self.phone_number = phone_number
        self.email = email

    def display_member_info(self):
        """Display the member's information."""
        print(
            f"Member ID: {self.member_id}\n"
            f"Name: {self.name}\n"
            f"Phone Number: {self.phone_number}\n"
            f"Email: {self.email}"
        )