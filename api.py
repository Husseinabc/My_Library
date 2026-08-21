from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from library import Library
from book import Book
from member import Member

from schemas import (
    BookCreate,
    BookUpdate,
    MemberCreate,
    MemberUpdate,
    LoanCreate,
    RegisterRequest,
)

from models import User
from database import SessionLocal
from repositories.user_repository import UserRepository

from security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)
from fastapi.responses import RedirectResponse
from google_oauth import oauth
from fastapi import Request
from starlette.middleware.sessions import SessionMiddleware
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


app = FastAPI(title="Library API")

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY"),
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")

library = Library()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    with SessionLocal() as session:
        user_repository = UserRepository(session)
        user = user_repository.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        return user


@app.get("/")
def root():
    return {"message": "Library API is running"}


# ============================================================
# Books
# ============================================================

@app.get("/books")
def get_books(current_user=Depends(get_current_user)):
    return library.view_all_books()


@app.get("/books/{book_id}")
def get_book(
    book_id: int,
    current_user=Depends(get_current_user)
):
    book = library.search_book(book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@app.post("/books", status_code=201)
def create_book(
    book_data: BookCreate,
    current_user=Depends(get_current_user)
):
    book = Book(
        book_data.book_id,
        book_data.title,
        book_data.author,
        book_data.publish_year
    )

    if not library.add_book(book):
        raise HTTPException(
            status_code=409,
            detail="Book ID already exists"
        )

    return book


@app.patch("/books/{book_id}")
def update_book(
    book_id: int,
    book_data: BookUpdate,
    current_user=Depends(get_current_user)
):
    book = library.search_book(book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    library.update_book(
        book,
        book_data.title,
        book_data.author,
        book_data.publish_year
    )

    return book


@app.delete("/books/{book_id}", status_code=204)
def delete_book(
    book_id: int,
    current_user=Depends(get_current_user)
):
    book = library.search_book(book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if not library.delete_book(book):
        raise HTTPException(
            status_code=409,
            detail="Cannot delete borrowed book"
        )


# ============================================================
# Members
# ============================================================

@app.get("/members")
def get_members(current_user=Depends(get_current_user)):
    return library.view_all_members()


@app.get("/members/{member_id}")
def get_member(
    member_id: int,
    current_user=Depends(get_current_user)
):
    member = library.search_member(member_id)

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    return member


@app.post("/members", status_code=201)
def create_member(
    member_data: MemberCreate,
    current_user=Depends(get_current_user)
):
    member = Member(
        member_data.member_id,
        member_data.name,
        member_data.phone_number,
        member_data.email
    )

    if not library.add_member(member):
        raise HTTPException(
            status_code=409,
            detail="Member ID already exists"
        )

    return member


@app.patch("/members/{member_id}")
def update_member(
    member_id: int,
    member_data: MemberUpdate,
    current_user=Depends(get_current_user)
):
    member = library.search_member(member_id)

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    library.update_member(
        member,
        member_data.name,
        member_data.phone_number,
        member_data.email
    )

    return member


@app.delete("/members/{member_id}", status_code=204)
def delete_member(
    member_id: int,
    current_user=Depends(get_current_user)
):
    member = library.search_member(member_id)

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    if not library.delete_member(member):
        raise HTTPException(
            status_code=409,
            detail="Cannot delete member with borrowed books"
        )


# ============================================================
# Loans
# ============================================================

@app.get("/loans")
def get_loans(current_user=Depends(get_current_user)):
    return library.view_borrowed_books()


@app.post("/loans", status_code=201)
def create_loan(
    loan_data: LoanCreate,
    current_user=Depends(get_current_user)
):
    member = library.search_member(loan_data.member_id)
    book = library.search_book(loan_data.book_id)

    if not member or not book:
        raise HTTPException(
            status_code=404,
            detail="Member or Book not found"
        )

    loan = library.borrow_book(member, book)

    if not loan:
        raise HTTPException(
            status_code=409,
            detail="Book is not available"
        )

    return loan


@app.post("/loans/{book_id}/return")
def return_book(
    book_id: int,
    current_user=Depends(get_current_user)
):
    book = library.search_book(book_id)

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    loan = library.return_book(book)

    if not loan:
        raise HTTPException(
            status_code=409,
            detail="This book is not currently borrowed"
        )

    return loan


# ============================================================
# Authentication
# ============================================================

@app.post("/auth/register", status_code=201)
def register(user_data: RegisterRequest):
    with SessionLocal() as session:
        user_repository = UserRepository(session)

        existing_user = user_repository.get_by_email(user_data.email)

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="Email already registered"
            )

        user = User(
            email=user_data.email,
            hashed_password=hash_password(user_data.password)
        )

        user = user_repository.create(user)

        return {
            "id": user.id,
            "email": user.email
        }


@app.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with SessionLocal() as session:
        user_repository = UserRepository(session)

        user = user_repository.get_by_email(form_data.username)

        if not user or not user.hashed_password:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        if not verify_password(
            form_data.password,
            user.hashed_password
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        access_token = create_access_token(user.id)

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }


@app.get("/auth/google")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth/google/callback")
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = token["userinfo"]

    google_id = user_info["sub"]
    email = user_info["email"]

    with SessionLocal() as session:
        user_repository = UserRepository(session)

        user = user_repository.get_by_email(email)

        if not user:
            user = User(
                email=email,
                google_id=google_id
            )
            user = user_repository.create(user)

        elif not user.google_id:
            user.google_id = google_id
            session.commit()

        access_token = create_access_token(user.id)

        return RedirectResponse(
        url=f"/frontend/index.html?token={access_token}"
        )