from pydantic import BaseModel


class BookCreate(BaseModel):
    book_id: int
    title: str
    author: str
    publish_year: int

class BookUpdate(BaseModel):
    title: str
    author: str
    publish_year: int


class MemberCreate(BaseModel):
    member_id: int
    name: str
    phone_number: str
    email: str


class MemberUpdate(BaseModel):
    name: str
    phone_number: str
    email: str


class LoanCreate(BaseModel):
    member_id: int
    book_id: int


class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str