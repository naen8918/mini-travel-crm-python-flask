# 🚀 Mini Travel CRM – Flask REST API

![Build](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![Status](https://img.shields.io/badge/status-in%20development-yellow)

> A secure, modular CRM system tailored for small travel agencies.  
> Built with Python, Flask, and SQLAlchemy, it enables efficient management of clients, trips, invoices, and payments — all protected with JWT authentication and role-based access control.

---
## 📌 Project Description

**Mini Travel CRM** is a lightweight REST API for managing customer interactions and bookings in a small travel agency. It includes full CRUD functionality, client notes, financial reports, and robust security for multi-role access. Ideal for backend portfolio projects, API design practice, and small business use cases.

---

## ✨ Key Features

- 🔐 **JWT Authentication** (`/register`, `/login`, `/me`)
- 👥 **Role-Based Access Control** (`admin`, `agent`, `analyst`)
- 📁 Full **CRUD Operations**: Clients, Trips, Invoices, Payments
- 🧾 **Client Notes** system: Add/update/delete internal notes per client
- 📊 **Reports API**: Monthly revenue, revenue by client, unpaid invoices
- 🔍 **Search/Filter Support** for Clients and Trips
- 🧱 Modular Flask app using Blueprints
- 🧪 **Postman-Ready** for full testing coverage
- 💾 Lightweight **SQLite** database + SQLAlchemy ORM

---

## 👥 Roles & Permissions

| Role     | Permissions                          |
|----------|--------------------------------------|
| `admin`  | Full access, including user cleanup  |
| `agent`  | Add/update business records          |
| `analyst`| Read-only access to reports          |

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
`GET /me` with header:

```http
Authorization: Bearer <access_token>
```

## 🗂️ Folder Structure

```bash
mini-travel-crm-python-flask/
│
├── app.py                  # Main entry point
├── config.py               # App config + DB + JWT secrets
├── .env                    # Local secrets (not pushed)
├── requirements.txt
│
├── models/                   # SQLAlchemy ORM Models
│   ├── client_note.py         # New: model for storing notes tied to clients                 
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

| Endpoint                     | Description                                |
| ---------------------------- | ------------------------------------------ |
| `/reports/invoice-summary`   | Paid, Pending, and Overdue invoice count   |
| `/reports/monthly-revenue`   | Monthly revenue by year & destination/year |
| `/reports/revenue-by-client` | Total revenue generated per client         |
| `/reports/unpaid-invoices`   | List of all unpaid invoices                |


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
    
1. Login via `/login` and store your `access_token`
2. Set Header:

    ```pgsql
    Authorization: Bearer <your_token>
    Content-Type: application/json
    ```
3. Use all `/clients`, `/trips`, `/invoices`, `/payments`, 
`/reports/`, and `/clients/<id>/notes` * endpoints.
---

## 📈 Future Improvements

| Feature                     | Description                          |
| --------------------------- | ------------------------------------ s|
| 📤 CSV/PDF Report Export    | Download reports easily             |
| 🖼️ Frontend UI (React/Vue) | User-friendly dashboard interface    |
| 🌍 Localization Support     | Multi-language CRM support          |
| 🛡️ Admin UI Panel          | Manage users and permissions via GUI |


---
## 👤 Author
### Nazgul Engvall
Backend-Focused System Developer
GitHub: [naen8918](https://github.com/naen8918)


## 📝 License

This project is licensed under the MIT License.
