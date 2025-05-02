# Mini Travel CRM (Python Flask Project)

This project is a minimal CRM (Customer Relationship Management) system designed for small travel agencies.  
Built using **Python**, **Flask**, and **SQLAlchemy**, this CRM handles client relationships, trips, invoices, payments, and revenue reporting.

---

## ✨ Features (Sprint 1–4)

- ✅ **Client Management** (Create, Read, Update, Delete)
- ✅ **Trip Management** (per client)
- ✅ **Invoice Handling** (linked to trips)
- ✅ **Payment Recording** (linked to invoices)
- ✅ **Get-by-ID endpoints** for clients, invoices, and payments
- ✅ **Revenue Reports** (monthly, per client, by destination)
- ✅ **Unpaid/Overdue Invoice Summary**
- ✅ **Overdue detection** logic for transparency
- ✅ **SQLite database** (`crm.db`) with ORM via SQLAlchemy
- ✅ Modular REST API structure using Blueprints
- ✅ Fully testable with **Postman**
- 🚀 Designed for future frontend dashboards and login system

---

## 🚀 Technologies Used

- **Python 3.11**
- **Flask** – lightweight web framework
- **Flask-SQLAlchemy** – ORM for database management
- **SQLite** – local embedded database
- **Postman** – API testing and debugging

---

## 🗂️ Project Structure

```bash
mini-travel-crm-python-flask/
│ 
├── app.py               # Main Flask app and blueprint registration
├── config.py            # Database configuration
├── requirements.txt     # Python Dependencies
├── .gitignore           # Git ignored files
├── README.md            # Project documentation
│
├── models/              # SQLAlchemy models
│   ├── client.py
│   ├── trip.py
│   ├── invoice.py
│   └── payment.py
│
├── routes/              # Flask Blueprints for modular routes(API endpoints)
│   ├── clients.py
│   ├── trips.py
│   ├── invoices.py
│   ├── payments.py
│   └── reports.py
│
├── static/              # Static frontend files (empty for now) 
└── templates/           # HTML templates (empty for now)

```

---

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

**4. Run the Flask app:**
   ```
   $env:FLASK_APP="app"
   flask run
   ```

**5. The server will start on:**
    ```
   (http://127.0.0.1:5000)
    ```
**6. Use Postman to test the API:**
    ```
-   - (POST /clients to add a new client)
-   - (GET /clients to list all clients)
+   - POST /clients – add a new client
+   - GET /clients – list all clients
    ```
## 🧑‍🎨 UI Preview (Invoice Summary Widget)

📋 Invoice Summary
✅ Paid: 3 invoices [IDs: 2, 4, 7]
⏳ Pending: 2 invoices [IDs: 5, 6]
⚠️ Overdue: 1 invoice [ID: 8]

- This widget will appear on the future admin dashboard and help identify financial risks and pending actions.

## 👤 Author
# Nazgul Engvall
Backend-focused System Developer
GitHub: naen8918

---

## 🚀 What's Next (Future Sprints)

- 🔐 Authentication System (admin login, route protection)
- 🧾 Export reports to CSV/PDF
- 📈 Frontend dashboard with charts and filters
- 🌐 Support for multiple languages (localization)
