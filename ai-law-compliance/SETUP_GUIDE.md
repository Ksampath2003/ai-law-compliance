# 🧒 Complete Beginner Setup Guide
### "I just have the ZIP file and nothing else installed"

Follow every step in order. Don't skip anything!

---

## PART 1 — Install the Tools You Need

You need to install 4 things. Do them one at a time.

---

### Step 1 — Install Git

Git is how you put code on GitHub.

1. Go to: **https://git-scm.com/downloads**
2. Click the big download button for your computer (Windows or Mac)
3. Open the file that downloaded and click **Next** through everything — the defaults are fine
4. When it's done, open a terminal:
   - **Windows:** Press the Windows key, type `cmd`, press Enter
   - **Mac:** Press Cmd+Space, type `terminal`, press Enter
5. Type this and press Enter:
   ```
   git --version
   ```
   You should see something like `git version 2.44.0` — that means it worked ✅

---

### Step 2 — Install Python

Python runs the backend of the app.

1. Go to: **https://www.python.org/downloads/**
2. Click the big yellow **Download Python 3.11.x** button
3. Open the installer
   - ⚠️ **IMPORTANT:** Check the box that says **"Add Python to PATH"** before clicking Install
4. Click **Install Now**
5. When done, in your terminal type:
   ```
   python --version
   ```
   You should see `Python 3.11.x` ✅

---

### Step 3 — Install Node.js

Node.js runs the frontend of the app.

1. Go to: **https://nodejs.org/**
2. Click the **LTS** version button (the left one — it says "Recommended")
3. Open the installer and click Next through everything
4. When done, in your terminal type:
   ```
   node --version
   ```
   You should see `v18.x.x` or higher ✅

---

### Step 4 — Install PostgreSQL

PostgreSQL is the database that stores the laws.

1. Go to: **https://www.postgresql.org/download/**
2. Click your operating system (Windows or macOS)
3. Download the installer from **EDB** (the first option)
4. Open the installer and click Next through everything
   - When it asks for a **password**, type: `password` (exactly this, lowercase)
   - When it asks for a **port**, leave it as `5432`
   - Leave everything else as default
5. When done, the PostgreSQL service starts automatically in the background ✅

---

## PART 2 — Set Up Your Accounts

---

### Step 5 — Create a GitHub Account

GitHub is where your code lives online.

1. Go to: **https://github.com**
2. Click **Sign up**
3. Enter your email, create a password, choose a username
4. Verify your email when they send you a confirmation

---

### Step 6 — Create an Anthropic Account & Get Your API Key

The API key lets the app use Claude AI for analysis.

1. Go to: **https://console.anthropic.com**
2. Click **Sign up** and create an account
3. Once logged in, click **API Keys** in the left sidebar
4. Click **Create Key**
5. Give it a name like `ai-law-app`
6. **Copy the key immediately** — it starts with `sk-ant-...`
   - ⚠️ You only see it once! Paste it somewhere safe like Notepad first.

---

## PART 3 — Set Up the Project

---

### Step 7 — Unzip the File

1. Find the `ai-law-compliance.zip` file you downloaded
2. Right-click it and click **Extract All** (Windows) or double-click it (Mac)
3. Choose a location you'll remember, like your Desktop or Documents folder
4. You should now have a folder called `ai-law-compliance`

---

### Step 8 — Create a GitHub Repository

1. Go to **https://github.com** and log in
2. Click the **+** button in the top right corner
3. Click **New repository**
4. Name it: `ai-law-compliance`
5. Leave it as **Public** (or Private if you prefer)
6. **Do NOT** check any boxes (no README, no .gitignore)
7. Click **Create repository**
8. You'll see a page with some code — keep this tab open, you'll need it in Step 10

---

### Step 9 — Open the Project Folder in Terminal

**Windows:**
1. Open the `ai-law-compliance` folder in File Explorer
2. Click on the address bar at the top (where it shows the folder path)
3. Type `cmd` and press Enter — a terminal opens in that folder

**Mac:**
1. Open Terminal (Cmd+Space → type "terminal")
2. Type `cd ` (with a space after), then drag the `ai-law-compliance` folder into the terminal window
3. Press Enter

To confirm you're in the right place, type:
```
ls
```
You should see files like `README.md`, `docker-compose.yml`, `backend`, `frontend` ✅

---

### Step 10 — Push the Code to GitHub

In your terminal (still inside the `ai-law-compliance` folder), type each of these lines one at a time, pressing Enter after each:

```
git init
```
```
git add .
```
```
git commit -m "Initial commit"
```
```
git branch -M main
```

Now go back to the GitHub tab from Step 8. Copy the line that looks like this (it'll have YOUR username):
```
git remote add origin https://github.com/YOUR-USERNAME/ai-law-compliance.git
```
Paste it in your terminal and press Enter. Then type:
```
git push -u origin main
```

It may ask for your GitHub username and password. For the password, use a **Personal Access Token** (not your account password):
1. Go to https://github.com/settings/tokens
2. Click **Generate new token (classic)**
3. Give it a name, check the **repo** checkbox
4. Click **Generate token** and copy it
5. Paste it as your password in the terminal

Refresh your GitHub page — your code should be there! ✅

---

## PART 4 — Configure and Run the App

---

### Step 11 — Create the Environment File

The `.env` file is where you put your secret keys. The app reads this file to know how to connect to the database and Claude AI.

In your terminal (inside `ai-law-compliance` folder):

**Windows:**
```
copy .env.example .env
```

**Mac:**
```
cp .env.example .env
```

Now open the `.env` file:
- **Windows:** Type `notepad .env` in terminal
- **Mac:** Type `open -e .env` in terminal

Find this line:
```
ANTHROPIC_API_KEY=sk-ant-...
```

Replace `sk-ant-...` with the actual API key you copied in Step 6. Save the file and close it.

---

### Step 12 — Set Up the Database

You need to create a database called `ai_law_compliance` in PostgreSQL.

**Windows:**
1. Press the Windows key and search for **pgAdmin 4** — open it
2. It will ask for the password you set during install — type `password`
3. In the left panel, right-click **Databases** → **Create** → **Database**
4. Name it `ai_law_compliance` and click **Save**

**Mac:**
In your terminal type:
```
psql -U postgres -c "CREATE DATABASE ai_law_compliance;"
```
If it asks for a password, type `password`

---

### Step 13 — Set Up the Backend

In your terminal, navigate to the backend folder:
```
cd backend
```

Create a virtual environment (this keeps the app's Python packages separate from your system):

**Windows:**
```
python -m venv venv
venv\Scripts\activate
```

**Mac:**
```
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` appear at the start of your terminal line — that means it worked ✅

Now install all the Python packages the app needs:
```
pip install -r requirements.txt
```
This will take 2-3 minutes. Lots of things will scroll by — that's normal.

Now set up the database tables:
```
alembic upgrade head
```
You should see `Running upgrade -> 0001_initial` ✅

Now seed the database with real AI laws:
```
python scripts/seed_laws.py
```
You should see 8 laws get added with ✅ checkmarks ✅

Now start the backend server:
```
uvicorn app.main:app --reload --port 8000
```

You should see:
```
INFO: Uvicorn running on http://127.0.0.1:8000
```

Leave this terminal window open! The backend is running. ✅

---

### Step 14 — Set Up the Frontend

Open a **brand new terminal window** (don't close the backend one).

Navigate to the frontend folder. From the `ai-law-compliance` folder:
```
cd frontend
```

Copy the frontend environment file:

**Windows:**
```
copy .env.local.example .env.local
```

**Mac:**
```
cp .env.local.example .env.local
```

Install the frontend packages:
```
npm install
```
This takes 1-2 minutes ✅

Start the frontend:
```
npm run dev
```

You should see:
```
ready - started server on 0.0.0.0:3000
```
✅

---

## PART 5 — Open the App!

### Step 15 — See It Work

Open your web browser and go to:

**http://localhost:3000**

You should see the AI Law Compliance app with 8 laws already loaded! 🎉

You can also see the API documentation at:

**http://localhost:8000/docs**

---

## 🛑 How to Stop the App

In each terminal window, press **Ctrl+C** to stop the server.

## ▶️ How to Start It Again Next Time

You don't need to redo all the steps — just:

**Terminal 1 (backend):**
```
cd ai-law-compliance/backend
source venv/bin/activate     ← Mac
venv\Scripts\activate        ← Windows
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 (frontend):**
```
cd ai-law-compliance/frontend
npm run dev
```

---

## 🆘 Common Problems & Fixes

| Problem | Fix |
|---|---|
| `python not found` | Try `python3` instead of `python` |
| `pip not found` | Try `pip3` instead of `pip` |
| `port already in use` | Another app is using that port. Add `--port 8001` to the uvicorn command |
| `database connection refused` | PostgreSQL isn't running. Search for "pgAdmin" or "PostgreSQL" in your apps and start it |
| `ANTHROPIC_API_KEY invalid` | Double-check you copied the full key into `.env` with no extra spaces |
| Frontend shows blank/error | Make sure the backend is running first on port 8000 |
| `permission denied` on Mac | Add `sudo` before the command (e.g., `sudo pip install ...`) |

---

## 🐳 Easier Option — Docker (Skip Steps 2, 3, 4, 12, 13, 14)

If you install Docker Desktop, you can skip setting up Python, Node, and PostgreSQL separately. Docker does it all for you in one command.

1. Download Docker Desktop: **https://www.docker.com/products/docker-desktop/**
2. Install it and start it (you'll see a whale icon in your taskbar)
3. Make sure your `.env` file has your `ANTHROPIC_API_KEY` (Step 11)
4. In the `ai-law-compliance` folder, run:
   ```
   docker-compose up --build
   ```
5. Wait ~3 minutes, then open **http://localhost:3000**

That's it! Docker handles everything automatically.
