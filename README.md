# CMS Backend (FastAPI)

## ✅ Project Overview
This is the backend for the Candidate Management System (CMS), built with **FastAPI**, **PostgreSQL**, and **Google OAuth 2.0 authentication**.  
The backend exposes APIs for login via Google and stores user info in the database.

---

## 📂 Project Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/suraj-suresh11/Cmsbackend_main_clean.git
cd Cmsbackend_main_clean
```

---

### 2️⃣ Create and Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 4️⃣ Create `.env` File
Create a `.env` file inside the root or `/app` directory with the following keys:
```
DATABASE_URL=postgresql+asyncpg://postgres:yourpassword@localhost:5432/yourdbname
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
FRONTEND_URL=http://localhost:3000
REDIRECT_URI=http://localhost:8000/auth/callback/google
SECRET_KEY=your-secret-jwt-key
SESSION_SECRET=your-session-secret
```

---

### 5️⃣ Google OAuth Setup
- Go to [Google Cloud Console](https://console.cloud.google.com/).
- Create a new project and navigate to **APIs & Services > Credentials**.
- Create **OAuth 2.0 Client ID** and set:
  - **Authorized redirect URIs**:
    - `http://localhost:8000/auth/callback/google`
    - `http://127.0.0.1:8000/auth/callback/google` (optional)
- Add the client ID and secret to your `.env` file.

---

### 6️⃣ Database Setup
- Ensure PostgreSQL is running and create the database:
```bash
createdb yourdbname
```

---

### 7️⃣ Run Alembic Migrations
```bash
alembic upgrade head
```

---

### 8️⃣ Run the FastAPI Server
```bash
uvicorn app.main:app --reload
```
- Access the backend via `http://127.0.0.1:8000`

---

## ✅ Auth Endpoint to test:
- [http://127.0.0.1:8000/auth/google](http://127.0.0.1:8000/auth/google)

---

### 👨‍💻 Contributions
For contributions or collaborations, feel free to create a pull request!

---
