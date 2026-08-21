from sqlalchemy import select
from sqlalchemy.orm import Session

from member import Member as DomainMember
from models import Member as MemberModel


class MemberRepository:
    """
    Handles database operations for members.

    Converts between the Domain Member and SQLAlchemy Member model.
    """

    def __init__(self, session: Session):
        self.session = session

    def add(self, member: DomainMember) -> DomainMember:
        """Save a domain Member in PostgreSQL."""

        db_member = MemberModel(
            name=member.name,
            phone_number=member.phone_number,
            email=member.email,
        )

        self.session.add(db_member)
        self.session.commit()
        self.session.refresh(db_member)

        member.member_id = db_member.id

        return member

    def get_by_id(self, member_id: int) -> DomainMember | None:
        """Get a member from PostgreSQL by ID."""

        statement = select(MemberModel).where(MemberModel.id == member_id)
        db_member = self.session.scalar(statement)

        if db_member is None:
            return None

        return self._to_domain(db_member)

    def get_all(self) -> list[DomainMember]:
        """Return all members from PostgreSQL."""

        statement = select(MemberModel)
        db_members = self.session.scalars(statement).all()

        return [self._to_domain(member) for member in db_members]

    def update(
        self,
        member: DomainMember
    ) -> DomainMember | None:
        """Update an existing member."""

        statement = select(MemberModel).where(
            MemberModel.id == member.member_id
        )

        db_member = self.session.scalar(statement)

        if db_member is None:
            return None

        db_member.name = member.name
        db_member.phone_number = member.phone_number
        db_member.email = member.email

        self.session.commit()
        self.session.refresh(db_member)

        return member

    def delete(
        self,
        member: DomainMember
    ) -> DomainMember | None:
        """Delete a member from PostgreSQL."""

        statement = select(MemberModel).where(
            MemberModel.id == member.member_id
        )

        db_member = self.session.scalar(statement)

        if db_member is None:
            return None

        self.session.delete(db_member)
        self.session.commit()

        return member

    @staticmethod
    def _to_domain(db_member: MemberModel) -> DomainMember:
        """Convert SQLAlchemy model into a domain Member."""

        return DomainMember(
            member_id=db_member.id,
            name=db_member.name,
            phone_number=db_member.phone_number,
            email=db_member.email,
        )