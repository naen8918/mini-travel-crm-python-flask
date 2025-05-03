# 🚀 Mini Travel CRM – Flask REST API

![Build](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![Status](https://img.shields.io/badge/status-in%20development-yellow)

> A lightweight CRM system tailored for small travel agencies.  
> Built with Python, Flask, and SQLAlchemy, it provides client, trip, invoice, and payment management — with JWT-based authentication and role-based access control for security.

---

## ✨ Key Features

- 🔐 **JWT Authentication** (Register, Login, `/me` endpoint)
- 👥 **Role-Based Access Control** (`admin`, `agent`, `analyst`)
- 📁 Full CRUD for **Clients, Trips, Invoices, Payments**
- 💰 **Reports API**: Revenue, unpaid invoices, invoice summaries
- 🧾 **Invoice Tracking**: Pending, Paid, Overdue
- 🧱 Modular architecture using Flask Blueprints
- 🧪 Ready for **Postman testing**
- 🗂️ Uses **SQLite** and **Flask-SQLAlchemy** for DB operations

---

## 👥 Roles & Permissions

| Role     | Description                             |
|----------|-----------------------------------------|
| `admin`  | Full access to all endpoints            |
| `agent`  | Can create/update business data         |
| `analyst`| Read-only access to financial reports   |

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
├── models/                 # SQLAlchemy ORM Models
│   ├── client.py
│   ├── trip.py
│   ├── invoice.py
│   └── payment.py
│
├── routes/                 # Business logic & API endpoints
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
| Endpoint                     | Description                              |
| ---------------------------- | ---------------------------------------- |
| `/reports/invoice-summary`   | Paid, Pending, and Overdue invoice count |
| `/reports/monthly-revenue`   | Monthly revenue by year & destination    |
| `/reports/revenue-by-client` | Total revenue generated per client       |
| `/reports/unpaid-invoices`   | List of all unpaid invoices              |


---

## 🔐 Protected Routes Summary

| Endpoint         | Method | Roles          |
| ---------------- | ------ | -------------- |
| `/clients`       | POST   | admin, agent   |
| `/clients/<id>`  | DELETE | admin          |
| `/trips`         | POST   | admin, agent   |
| `/trips/<id>`    | DELETE | admin          |
| `/invoices`      | POST   | admin, agent   |
| `/invoices/<id>` | DELETE | admin          |
| `/payments`      | POST   | admin, agent   |
| `/payments/<id>` | DELETE | admin          |
| `/reports/*`     | GET    | admin, analyst |

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
    
1. Login via `/login`, store token
2. Set Header:

    ```pgsql
    Authorization: Bearer <your_token>
    Content-Type: application/json
    ```
3. Use all `/clients`, `/trips`, `/invoices`, `/payments`, and `/reports/`* endpoints.
---

## 📈 Future Improvements
- 📤 Export reports as CSV or PDF
- 🖼️ Build a frontend (React/Vue)
- 🌍 Localization support (multi-language)
- 🛡️ Admin UI panel for user/role management
---
## 👤 Author
### Nazgul Engvall
Backend-Focused System Developer
GitHub: [naen8918](https://github.com/naen8918)


## 📝 License

This project is licensed under the MIT License.
