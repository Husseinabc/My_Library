const API_URL = "http://127.0.0.1:8000";
const loginSection = document.getElementById("login-section");
const dashboardSection = document.getElementById("dashboard-section");
const loginForm = document.getElementById("login-form");
const googleLogin = document.getElementById("google-login");
const logoutButton = document.getElementById("logout");

const booksList = document.getElementById("books-list");
const membersList = document.getElementById("members-list");
const loansList = document.getElementById("loans-list");


// ============================================================
// Google JWT
// ============================================================

const params = new URLSearchParams(window.location.search);
const googleToken = params.get("token");

if (googleToken) {
    localStorage.setItem("access_token", googleToken);
    window.history.replaceState({}, document.title, window.location.pathname);
}


// ============================================================
// Authentication
// ============================================================

loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.detail || "Login failed");
            return;
        }

        localStorage.setItem("access_token", data.access_token);

        showDashboard();
        loadAll();

    } catch (error) {
        alert("Could not connect to the server.");
        console.error(error);
    }
});


googleLogin.addEventListener("click", () => {
    window.location.href = `${API_URL}/auth/google`;
});


logoutButton.addEventListener("click", () => {
    localStorage.removeItem("access_token");

    dashboardSection.classList.add("hidden");
    loginSection.classList.remove("hidden");
});


function getToken() {
    return localStorage.getItem("access_token");
}


function authHeaders() {
    return {
        "Authorization": `Bearer ${getToken()}`,
        "Content-Type": "application/json"
    };
}


function showDashboard() {
    loginSection.classList.add("hidden");
    dashboardSection.classList.remove("hidden");
}


async function apiRequest(url, options = {}) {
    const response = await fetch(url, {
        ...options,
        headers: {
            ...authHeaders(),
            ...(options.headers || {})
        }
    });

    if (response.status === 204) {
        return null;
    }

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Request failed");
    }

    return data;
}


// ============================================================
// BOOKS
// ============================================================

async function loadBooks() {
    try {
        const books = await apiRequest(`${API_URL}/books`);

        booksList.innerHTML = "";

        books.forEach(book => {
            const row = document.createElement("div");
            row.className = "item-row";

            row.innerHTML = `
                <div class="item-info">
                    <strong>${book.title}</strong>
                    <span>
                        ID: ${book.book_id ?? book.id}
                        | Author: ${book.author}
                        | Year: ${book.publish_year}
                        | ${book.is_available ? "Available" : "Borrowed"}
                    </span>
                </div>

                <div>
                    <button class="action-btn edit-btn"
                        onclick="editBook(${book.book_id ?? book.id})">
                        Edit
                    </button>

                    <button class="action-btn delete-btn"
                        onclick="deleteBook(${book.book_id ?? book.id})">
                        Delete
                    </button>

                    <button class="action-btn return-btn"
                        onclick="borrowBookPrompt(${book.book_id ?? book.id})">
                        Borrow
                    </button>

                    <button class="action-btn return-btn"
                        onclick="returnBook(${book.book_id ?? book.id})">
                        Return
                    </button>
                </div>
            `;

            booksList.appendChild(row);
        });

    } catch (error) {
        alert(error.message);
    }
}


function showBookForm(book = null) {
    document.getElementById("book-form").classList.remove("hidden");

    document.getElementById("book-id").value = book
        ? (book.book_id ?? book.id)
        : "";

    document.getElementById("book-title").value =
        book ? book.title : "";

    document.getElementById("book-author").value =
        book ? book.author : "";

    document.getElementById("book-year").value =
        book ? book.publish_year : "";
}


function hideBookForm() {
    document.getElementById("book-form").classList.add("hidden");
}

let editingBookId = null;

function showBookForm(book = null) {
    document.getElementById("book-form").classList.remove("hidden");

    editingBookId = book
        ? (book.book_id ?? book.id)
        : null;

    document.getElementById("book-id").value =
        book ? editingBookId : "";

    document.getElementById("book-title").value =
        book ? book.title : "";

    document.getElementById("book-author").value =
        book ? book.author : "";

    document.getElementById("book-year").value =
        book ? book.publish_year : "";
}

function hideBookForm() {
    document.getElementById("book-form").classList.add("hidden");

    editingBookId = null;
}

async function saveBook() {
    const bookId = Number(
        document.getElementById("book-id").value
    );

    const title =
        document.getElementById("book-title").value;

    const author =
        document.getElementById("book-author").value;

    const publish_year =
        Number(document.getElementById("book-year").value);

    try {
        if (editingBookId !== null) {

            await apiRequest(`${API_URL}/books/${editingBookId}`, {
                method: "PATCH",
                body: JSON.stringify({
                    title,
                    author,
                    publish_year
                })
            });

        } else {

            await apiRequest(`${API_URL}/books`, {
                method: "POST",
                body: JSON.stringify({
                    book_id: bookId,
                    title,
                    author,
                    publish_year
                })
            });
        }

        hideBookForm();
        loadBooks();

    } catch (error) {
        alert(error.message);
    }
}

async function editBook(id) {
    try {
        const book = await apiRequest(`${API_URL}/books/${id}`);
        showBookForm(book);
    } catch (error) {
        alert(error.message);
    }
}


async function deleteBook(id) {
    if (!confirm("Delete this book?")) {
        return;
    }

    try {
        await apiRequest(`${API_URL}/books/${id}`, {
            method: "DELETE"
        });

        loadBooks();

    } catch (error) {
        alert(error.message);
    }
}


async function borrowBookPrompt(bookId) {
    const memberId = prompt("Enter Member ID:");

    if (!memberId) {
        return;
    }

    try {
        await apiRequest(`${API_URL}/loans`, {
            method: "POST",
            body: JSON.stringify({
                member_id: Number(memberId),
                book_id: Number(bookId)
            })
        });

        alert("Book borrowed successfully.");

        loadBooks();
        loadLoans();

    } catch (error) {
        alert(error.message);
    }
}


async function returnBook(bookId) {
    try {
        await apiRequest(`${API_URL}/loans/${bookId}/return`, {
            method: "POST"
        });

        alert("Book returned successfully.");

        loadBooks();
        loadLoans();

    } catch (error) {
        alert(error.message);
    }
}


// ============================================================
// MEMBERS
// ============================================================

async function loadMembers() {
    try {
        const members = await apiRequest(`${API_URL}/members`);

        membersList.innerHTML = "";

        members.forEach(member => {
            const id = member.member_id ?? member.id;

            const row = document.createElement("div");
            row.className = "item-row";

            row.innerHTML = `
                <div class="item-info">
                    <strong>${member.name}</strong>
                    <span>
                        ID: ${id}
                        | Phone: ${member.phone_number}
                        | Email: ${member.email}
                    </span>
                </div>

                <div>
                    <button class="action-btn edit-btn"
                        onclick="editMember(${id})">
                        Edit
                    </button>

                    <button class="action-btn delete-btn"
                        onclick="deleteMember(${id})">
                        Delete
                    </button>
                </div>
            `;

            membersList.appendChild(row);
        });

    } catch (error) {
        alert(error.message);
    }
}


function showMemberForm(member = null) {
    document.getElementById("member-form").classList.remove("hidden");

    document.getElementById("member-id").value =
        member ? (member.member_id ?? member.id) : "";

    document.getElementById("member-name").value =
        member ? member.name : "";

    document.getElementById("member-phone").value =
        member ? member.phone_number : "";

    document.getElementById("member-email").value =
        member ? member.email : "";
}


function hideMemberForm() {
    document.getElementById("member-form").classList.add("hidden");
}


async function saveMember() {
    const id = document.getElementById("member-id").value;
    const name = document.getElementById("member-name").value;
    const phone_number =
        document.getElementById("member-phone").value;
    const email =
        document.getElementById("member-email").value;

    try {
        if (id) {
            await apiRequest(`${API_URL}/members/${id}`, {
                method: "PATCH",
                body: JSON.stringify({
                    name,
                    phone_number,
                    email
                })
            });
        } else {
            await apiRequest(`${API_URL}/members`, {
                method: "POST",
                body: JSON.stringify({
                    member_id: Number(
                        prompt("Enter Member ID:")
                    ),
                    name,
                    phone_number,
                    email
                })
            });
        }

        hideMemberForm();
        loadMembers();

    } catch (error) {
        alert(error.message);
    }
}


async function editMember(id) {
    try {
        const member =
            await apiRequest(`${API_URL}/members/${id}`);

        showMemberForm(member);

    } catch (error) {
        alert(error.message);
    }
}


async function deleteMember(id) {
    if (!confirm("Delete this member?")) {
        return;
    }

    try {
        await apiRequest(`${API_URL}/members/${id}`, {
            method: "DELETE"
        });

        loadMembers();

    } catch (error) {
        alert(error.message);
    }
}


// ============================================================
// LOANS
// ============================================================

async function loadLoans() {
    try {
        const loans = await apiRequest(`${API_URL}/loans`);

        loansList.innerHTML = "";

        loans.forEach(loan => {
            const bookId =
                loan.book_id ??
                loan.book?.book_id ??
                loan.book?.id;

            const memberId =
                loan.member_id ??
                loan.member?.member_id ??
                loan.member?.id;

            const row = document.createElement("div");
            row.className = "item-row";

            row.innerHTML = `
                <div class="item-info">
                    <strong>Book ID: ${bookId}</strong>
                    <span>Member ID: ${memberId}</span>
                </div>

                <button class="action-btn return-btn"
                    onclick="returnBook(${bookId})">
                    Return
                </button>
            `;

            loansList.appendChild(row);
        });

    } catch (error) {
        alert(error.message);
    }
}


// ============================================================
// LOAD EVERYTHING
// ============================================================

function loadAll() {
    loadBooks();
    loadMembers();
    loadLoans();
}


// Google login
if (googleToken) {
    showDashboard();
    loadAll();
}