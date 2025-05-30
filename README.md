# 🚀 Mini Travel CRM – Flask REST API

![Build](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![Status](https://img.shields.io/badge/status-in%20development-yellow)

> A secure, modular CRM system tailored for small travel agencies.  
> Built with Python, Flask, and SQLAlchemy, it enables efficient management of clients, trips, invoices, and payments — all protected with JWT authentication and role-based access control.

---
## 📌 Project Description

**Mini Travel CRM** is a lightweight REST API for managing customer interactions and bookings in a small travel agency. It includes: 
- ✅ Full CRUD functionality
- 🔐 Secure user authentication & role management
- 🧾 Internal note-taking per client
- 📊 Financial and client reporting
- 🧠 Frontend-ready endpoints for dropdowns & user data

---

## ✨ Key Features

- 🔐 **JWT Authentication** (`/register`, `/login`, `/me`)
- 👥 **Role-Based Access Control** (`admin`, `agent`, `analyst`)
- 🔑 **User Management** (list all users via `/users`, restrict to admin)
- 📁 Full **CRUD Operations**: Clients, Trips, Invoices, Payments
- 🧾 **Client Notes** system: Add/update/delete internal notes
- 📊 **Reports API**: Monthly revenue, revenue by client, unpaid invoices
- 🌐 **Public Role List API** (`/roles`) for frontend dropdowns
- 🔍 **Search/Filter**: Filter clients and trips by name/date/etc.
- 🧱 Modular Flask app using Blueprints
- 🧪 **Postman-Ready** with protected route testing
- 💾 Lightweight **SQLite** database + SQLAlchemy ORM

---

## 👥 Roles & Permissions

| Role     | Description                          |
|----------|--------------------------------------|
| `admin`  | Full access + user management        |
| `agent`  | Add/update business records          |
| `analyst`| Read-only access to reporting APIs   |

---

## 🔐 Authentication Overview

### ✅ Register
`POST /register`
```json
{
  "username": "admin_user",
  "password": "securepass",
  "role": "admin" // optional, defaults to agent
}
```

## 🔑 Login
`POST /login`

## Returns a token:
```json
{
  "access_token": "eyJhbGciOi..."
}
```

## 🔍 Get Current User
`GET /me` (requires JWT header):

```http
Authorization: Bearer <access_token>
```

🧑‍💼 Get All Users (Admin Only)
`GET /users`
Returns list of all registered users with their ID, username, and role.

🧩 Get Available Roles
`GET /roles`
Returns a list of available roles: ["admin", "agent", "analyst"]. Ideal for frontend dropdown menus.


## 🗂️ Folder Structure

```bash
mini-travel-crm-python-flask/
│
├── app.py                  # Main App entry point
├── config.py               # DB, JWT secrets, roles config
├── .env                    # Local secrets (not committed)
├── requirements.txt
│
├── models/                   # SQLAlchemy ORM Models
│   ├── client_note.py         # model for storing notes tied to clients                 
│   ├── client.py
│   ├── trip.py
│   ├── invoice.py
│   └── payment.py
│
├── routes/                 # Business logic & API endpoints
│   ├── client_notes.py        # Client interaction tracking
│   ├── clients.py
│   ├── trips.py
│   ├── invoices.py
│   ├── payments.py
│   └── reports.py
│
├── auth/                   # Auth system
│   ├── models.py
│   ├── routes.py
│   ├── utils.py
│   └── permissions.py

```
---

## 📊 Reporting API

| Endpoint                            | Description                                    |
| ----------------------------------- | ---------------------------------------------- |
| `/reports/invoice-summary`          | JSON summary: Paid, Pending, Overdue invoices  |
| `/reports/monthly-revenue`          | JSON revenue grouped by month/year/destination |
| `/reports/revenue-by-client`        | JSON revenue totals per client                 |
| `/reports/unpaid-invoices`          | JSON list of all unpaid invoices               |
| `/reports/invoice-summary/export`   | **CSV export** of invoice summary              |
| `/reports/monthly-revenue/export`   | **CSV export** of monthly revenue              |
| `/reports/revenue-by-client/export` | **CSV export** of revenue per client           |
| `/reports/unpaid-invoices/export`   | **CSV export** of unpaid invoices              |


---

## 🔐 Protected Routes Summary

| Endpoint                   | Method | Roles          |
| -------------------------- | ------ | -------------- |
| `/clients`                 | POST   | admin, agent   |
| `/clients/<id>`            | DELETE | admin          |
| `/trips`                   | POST   | admin, agent   |
| `/trips/<id>`              | DELETE | admin          |
| `/invoices`                | POST   | admin, agent   |
| `/invoices/<id>`           | DELETE | admin          |
| `/payments`                | POST   | admin, agent   |
| `/payments/<id>`           | DELETE | admin          |
| `/clients/<id>/notes`      | POST   | admin, agent   |
| `/clients/<id>/notes/<id>` | PATCH  | admin, agent   |
| `/clients/<id>/notes/<id>` | DELETE | admin          |
| `/reports/*`               | GET    | admin, analyst |
| `/users`                   | GET    | admin only     |

---

## 📦 Quick Start (Windows)
```bash
# Clone the repo
git clone https://github.com/naen8918/mini-travel-crm-python-flask.git
cd mini-travel-crm-python-flask

# Create & activate a virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set secrets in .env
echo SECRET_KEY=your-secure-key > .env
echo JWT_SECRET_KEY=your-jwt-key >> .env

# Run the app
$env:FLASK_APP="app"
flask run
```

---

## 🧪 Postman Testing Instructions
    
1. Register och login to get your `access_token`
2. Set Headers in Postman:

    ```pgsql
    Authorization: Bearer <your_token>
    Content-Type: application/json
    ```
3. Use all endpoints: `/clients`, `/trips`, `/invoices`, `/payments`, `/reports/`, `/clients/<id>/notes`, `/me`, `/users`, `/roles`, etc.
---


## 🌟 Future Improvements

| Feature                     | Description                          |
|-----------------------------|--------------------------------------|
| 📤 PDF Export Support       | Extend reporting options beyond CSV  |
| 🖼️ Frontend UI              | React/Vue dashboard with Auth        |
| 🌍 Multi-language Support   | Localization-ready content           |
| 🛡️ Admin Panel             | Full user management via GUI         |


---
## 👤 Author
### Nazgul Engvall
Backend-Focused System Developer
GitHub: [naen8918](https://github.com/naen8918)


## 📝 License

This project is licensed under the MIT License. Feel free to use and adapt it for your own portfolio or business needs.

## 🧠 Ideal For

- Backend portfolio projects
- Flask/REST API architecture practice
- Small travel businesses needing a CRM tool
