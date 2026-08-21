from sqlalchemy import select

from models import User


class UserRepository:

    def __init__(self, session):
        self.session = session

    def get_by_email(self, email: str):
        return self.session.scalar(
            select(User).where(User.email == email)
        )

    def get_by_id(self, user_id: int):
        return self.session.get(User, user_id)

    def create(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user