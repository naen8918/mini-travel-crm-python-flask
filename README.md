# Mini Travel CRM (Python Flask Project)

This project is a minimal CRM (Customer Relationship Management) system designed for small travel agencies.  
Built using **Python**, **Flask**, and **SQLAlchemy**, this CRM handles client relationships, trips, invoices, and payments.

---

## ✨ Features (Sprint 1–3)

- ✅ **Client Management** (Create, Read, Update, Delete)
- ✅ **Trip Tracking** linked to each client
- ✅ **Invoice Handling** per trip (issue, due, status, amount)
- ✅ **Payment Recording** per invoice
- ✅ SQLite database backend (`crm.db`)
- ✅ Modular project structure with Blueprints
- ✅ RESTful API design, fully testable with Postman
- ✅ Ready for future expansions: reporting, login, dashboard
---

## 🚀 Technologies Used

- **Python 3.11**
- **Flask** (micro web framework)
- **Flask-SQLAlchemy** (ORM)
- **SQLite** (local embedded database)
- **Postman** (API testing)

---

## 🗂️ Project Structure

```bash
mini-travel-crm-python-flask/
│ 
├── app.py               # Main Flask application
├── config.py            # Database configuration
├── requirements.txt     # Dependencies
├── .gitignore           # Git ignored files
├── README.md            # Project documentation
│
├── models/              # SQLAlchemy models
│   ├── client.py
│   ├── trip.py
│   ├── invoice.py
│   └── payment.py
│
├── routes/              # Flask Blueprints (API endpoints)
│   ├── clients.py
│   ├── trips.py
│   ├── invoices.py
│   └── payments.py
│
├── static/              # Static files - Frontend static files (empty for now) 
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

## 🧪 API Usage (Summary)

### 📁 Clients
- `POST /clients` – Create a new client
- `GET /clients` – List all clients
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
- `PATCH /invoices/<id>` – Update invoice
- `DELETE /invoices/<id>` – Delete invoice

### 💳 Payments
- `POST /payments` – Record a payment
- `GET /payments/<invoice_id>` – List payments for an invoice
- `PATCH /payments/<id>` – Update payment
- `DELETE /payments/<id>` – Delete payment

## 📋 How to Run the Project

**1. Clone the repository:**

   ```bash
   git clone https://github.com/naen8918/mini-travel-crm-python-flask.git
   cd mini-travel-crm-python-flask
   ```

**2. Create and activate virtual environment:**

   ```
   python -m venv venv
   .\venv\Scripts\activate     # For Windows
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

## 👤 Author

## Nazgul Engvall
Backend-focused System Developer
GitHub: naen8918

---

## 🚀 What's Next (Sprint 4)

- 📊 Reporting Dashboard (unpaid invoices, revenue, top clients)
- 🔐 Authentication System (admin login, route protection)
