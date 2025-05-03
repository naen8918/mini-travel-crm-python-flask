# Mini Travel CRM (Python Flask Project)

This project is a minimal CRM (Customer Relationship Management) system designed for small travel agencies.  
Built using **Python**, **Flask**, and **SQLAlchemy**, this CRM handles client relationships, trips, invoices, payments, and revenue reporting.

---

## ✨ Features (Sprint 1–4)

- ✅ **Client Management** (Create, Read, Update, Delete)
- ✅ **Trip Management** (per client)
- ✅ **Invoice Handling** (linked to trips)
- ✅ **Payment Recording** (linked to invoices)
- ✅ **JWT Authentication System** (register/login, token-based access)
- ✅ **Role-Based Access Control** (admin / agent / analyst)
- ✅ **Get-by-ID endpoints** for clients, invoices, and payments
- ✅ **Revenue Reports** (monthly, per client, by destination)
- ✅ **Unpaid/Overdue Invoice Summary**
- ✅ **/me Endpoint** to inspect current user
- ✅ **SQLite database** (`crm.db`) with ORM via SQLAlchemy
- ✅ Modular REST API structure using Blueprints
- ✅ Fully testable with **Postman**

---

## 👥 User Roles

| Role     | Permissions |
|----------|-------------|
| `admin`  | Full access: create/update/delete everything |
| `agent`  | Create & update clients, trips, invoices, payments |
| `analyst`| View reports only |

---

## 🚀 Technologies Used

- **Python 3.11**
- **Flask** – lightweight web framework
- **Flask-JWT-Extended** – authentication
- **Flask-SQLAlchemy** – ORM for database management
- **SQLite** – local embedded database
- **Postman** – API testing and debugging
- **dotenv** – manage environment secrets securely
---

## 🗂️ Project Structure

```bash
mini-travel-crm-python-flask/
│
├── app.py                  # Main Flask app and blueprint registration
├── config.py               # Database configuration
├── requirements.txt        # Python Dependencies
├── .gitignore              # Git ignored files
├── README.md               # Project documentation
├── .env                    # Environment secrets (JWT keys)
│
├── models/                 # SQLAlchemy models
│   ├── client.py
│   ├── trip.py
│   ├── invoice.py
│   └── payment.py
│
├── routes/                # Flask Blueprints for modular routes(API endpoints)
│   ├── clients.py
│   ├── trips.py
│   ├── invoices.py
│   ├── payments.py
│   └── reports.py
│
├── auth/                   # Authentication module
│   ├── models.py
│   ├── routes.py
│   ├── utils.py
│   └── permissions.py
│
├── static/                # Static frontend files (empty for now) 
└── templates/             # HTML templates (empty for now)
```

## 🔐 Protected Routes & Permissions

| Endpoint                | Roles          | Description              |
| ----------------------- | -------------- | ------------------------ |
| `POST /clients`         | admin, agent   | Create new client        |
| `DELETE /clients/<id>`  | admin          | Delete a client          |
| `POST /trips`           | admin, agent   | Create trip              |
| `DELETE /trips/<id>`    | admin          | Delete trip              |
| `POST /invoices`        | admin, agent   | Create invoice           |
| `DELETE /invoices/<id>` | admin          | Delete invoice           |
| `POST /payments`        | admin, agent   | Record payment           |
| `DELETE /payments/<id>` | admin          | Delete payment           |
| `GET /reports/*`        | admin, analyst | Access financial reports |

---

## 📊 Reporting API
🧾 `/reports/invoice-summary`
Shows how many invoices are Paid / Pending / Overdue.

📅 `/reports/monthly-revenue?year=2025&destination=Rome`
Revenue by month/year and destination.

💼 `/reports/revenue-by-client`
Total revenue per client.

❌ `/reports/unpaid-invoices`
Lists invoices not yet marked as Paid.

---

## 🔐 Authentication API

### ✅ Register
**POST** `/register`
```json
{
  "username": "admin_user",
  "password": "securepass",
  "role": "admin"  // Optional, defaults to "agent"
}
```
## 🔑 Login
**POST** `/login`
```json
{
  "username": "admin_user",
  "password": "securepass"
}
```
## Returns:
```json
{
  "access_token": "eyJhbGciOi..."
}
```
## 🔍 Get Current User
**GET** `/me`
Header: Authorization: Bearer <access_token>

## Response:
```json
{
  "user_id": "1",
  "role": "admin"
}
```
## 🧪 API Usage Examples

### 📌 Add a New Client
**POST** `/clients`
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "123456789",
  "company": "Global Travels"
}
```
### 📌 Create a Trip
**POST** `/trips`
```json
{
  "destination": "Paris",
  "start_date": "2025-06-01",
  "end_date": "2025-06-07",
  "price": 1200.00,
  "notes": "Flight and hotel included",
  "client_id": 1
}
```
### 📌 Create an Invoice
**POST** `/invoices`
```json
{
  "trip_id": 1,
  "issue_date": "2025-06-01",
  "due_date": "2025-06-15",
  "amount": 1200.00,
  "status": "Pending"
}
```
### 📌 Get Invoices for a Trip
**GET** `/invoices/1`

## 📌 Record a Payment
**POST** `/payments`
```json
{
  "invoice_id": 1,
  "payment_date": "2025-06-10",
  "amount": 1200.00,
  "payment_method": "Credit Card"
}
```
## 📌 Get Payments for an Invoice
**GET** `/payments/1`

## 🧪 API Endpoints Usage (Summary)

### 📁 Clients
- `POST /clients` – Create a new client
- `GET /clients` – List all clients
- `GET /clients/<id>` – Get specific client
- `PATCH /clients/<id>` – Update a client
- `DELETE /clients/<id>` – Delete a client

### ✈️ Trips
- `POST /trips` – Create a new trip
- `GET /trips` – List all trips
- `PATCH /trips/<id>` – Update a trip
- `DELETE /trips/<id>` – Delete a trip

### 🧾 Invoices
- `POST /invoices` – Create an invoice
- `GET /invoices/<trip_id>` – List invoices for a trip
- `GET /invoices/<id>` – Get specific invoice
- `PATCH /invoices/<id>` – Update invoice
- `DELETE /invoices/<id>` – Delete invoice

### 💳 Payments
- `POST /payments` – Record a payment
- `GET /payments/<invoice_id>` – List payments for an invoice
- `GET /payments/<id>` – Get specific payment
- `PATCH /payments/<id>` – Update payment
- `DELETE /payments/<id>` – Delete payment

## 📊 Reporting API (Sprint 4)

🧾 `/reports/invoice-summary`
- Overview of all invoices:
  - How many are Paid, Pending, or Overdue
  - Invoice IDs per category

# Example output:
```json
{
  "total_paid": 1,
  "paid_invoice_ids": [8],
  "total_pending": 5,
  "pending_invoice_ids": [1, 2, 3],
  "total_overdue": 2,
  "overdue_invoice_ids": [4, 5]
}
```

📅 `/reports/monthly-revenue`
- Returns revenue grouped by month and year.
- Optional filters:
  - `?year=2025`
  - `?destination=Rome`
```json
[
  {
    "year": 2025,
    "month": 6,
    "destination": "Rome",
    "total_revenue": 2200.0
  }
]
```
💼 `/reports/revenue-by-client`
- Summarizes how much revenue each client generated.
```json
[
  {
    "client_id": 1,
    "client_name": "John Doe",
    "total_revenue": 3700.0
  }
]
```
❌ `/reports/unpaid-invoices`
- Shows all invoices where status is not marked "Paid".


## 📋 How to Run the Project

**1. Clone the repository:**

   ```bash
   git clone https://github.com/naen8918/mini-travel-crm-python-flask.git
   cd mini-travel-crm-python-flask
   ```

**2. Create and activate virtual environment:**

   ```
   python -m venv venv
   .\venv\Scripts\activate     # On Windows
   ``` 

**3. Install the required dependencies:**

   ```
   pip install -r requirements.txt
   ```

**4. Set environment variables in .env**

  ```
   SECRET_KEY=your-very-secure-flask-key
   JWT_SECRET_KEY=your-even-more-secure-jwt-key
  ```

**5.Run the Flask app:**

  ```
   $env:FLASK_APP="app"
   flask run
   ```

**6. The server will start on:**

    ```
   (http://127.0.0.1:5000)
    ```

**7. Use Postman to test the API:**
    
- Use **POST** ´/register´ and **POST** ´/login´ to get access token.
- Add this to headers:
      `Authorization: Bearer <your_token_here>`
      `Content-Type: application/json`

-   - (POST /clients to add a new client)
-   - (GET /clients to list all clients)
+   - POST /clients – add a new client
+   - GET /clients – list all clients

## 🧑‍🎨 UI Preview (Future)
- 📋 Invoice Summary Widget
- ✅ Paid: [IDs]
- ⏳ Pending: [IDs]
- ⚠️ Overdue: [IDs]
***This will appear in admin dashboard.*** 

---

## 👤 Author
# Nazgul Engvall
Backend-focused System Developer
GitHub: naen8918

---

## 🚀 What's Next (Future Sprints)

- 🧾 Export reports to CSV/PDF
- 📈 Frontend dashboard with charts and filters (React/Vue)
- 🌐 Support for multiple languages (localization)
- 🔒 Admin panel for user creation

